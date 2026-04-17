from bson import ObjectId, json_util
import ctypes
import json
import traceback
from pprint import pprint

from cerver.types import String
from cerver.utils import cerver_log_success
from cerver.utils import cerver_log_error
from cerver.utils import cerver_log_warning

from cerver.http import validate_body_value_exists

from controllers.utils import handle_body_input
from controllers.brigada import brigada_exist
from controllers.simulacros import simulacros_exist

from models.tramite import Tramite
from models.tramite import TRAMITE_CREADO
from models.tramite import TRAMITE_CON_BRIGADAS
from models.tramite import TRAMITE_CON_SIMULACROS
from models.tramite import TRAMITE_COMPLETO
from models.tramite import TRAMITE_BORRADO

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_tramites(tramites):
    response = dict ()

    for tramite in tramites:
        response[str(tramite["_id"])] = tramite["date"]

    return response

def tramites_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		tramites = Tramite.find(
			values,
			parse=False
		)

		if (tramites):
			result = json_util.dumps(build_results_tramites(tramites))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def tramites_read_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))

	return values

def tramites_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, tramites_read_handle_input, errors
		)

		if (not errors):
			error, result = tramites_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create tramit!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def tramite_handle_input (loaded_json: dict, errors: dict):
	values = dict ()

	values["estatus"] = validate_body_value_exists (loaded_json, "estatus", errors)

	return values

def  tramite_create_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	values["usuario"] = ObjectId (validate_body_value_exists (loaded_json, "usuario", errors))
	values["titulo"] = validate_body_value_exists (loaded_json, "titulo", errors)

	values.update (tramite_handle_input (loaded_json, errors))

	return values

def tramite_create_validate (values: dict, errors: dict):
	result = True

	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["titulo"] = values["titulo"]

	tramite_cursor = Tramite.find(
		query,
		parse=False
	)
	
	for tramite in tramite_cursor:
		errors["titulo"] = "Tramite already exists!"
		result = False
		break
		
	return result

def tramite_create_internal (values: dict):
	tramite_id = None
	
	try:
		tramite = Tramite(**values)

		tramite_id = str(tramite.save ())

		cerver_log_success (
			f"Tramite creado {tramite_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return tramite_id

def tramite_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	tramite_id = None

	try:
		values = handle_body_input (
			request, tramite_create_handle_input, errors
		)
		
		if (not errors):
			if (tramite_create_validate (values, errors)):
				tramite_id = tramite_create_internal (values)
	
	except:
		cerver_log_error (b"Failed to create tramit!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, tramite_id

def tramite_search (tramite_id):
	
	tramite = Tramite.find_by_id(
		tramite_id,
		parse=False
	)

	return tramite

def tramite_update_estatus (tramite, estatus):
	
	values = {
			'estatus': estatus
		}
	tramite_id = tramite['_id']
	updated = Tramite.update (
		{
			"_id": tramite_id
		},
		{
			"$set": values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated tramit {tramite_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update tramit {tramite_id} db record!".encode ("utf-8")
		)


def tramite_correct_status (values, errors):
	result = False

	brigada = brigada_exist (values)
	simulacros = simulacros_exist (values)

	if brigada:
		if simulacros:
			estatus = TRAMITE_COMPLETO
			result = True
		else:
			estatus = TRAMITE_CON_BRIGADAS
			errors['data'] = "Falta programar simulacros!"
			
	elif simulacros:
		estatus = TRAMITE_CON_SIMULACROS
		errors['data'] = "Falta armar la brigada!"
	
	else:
		estatus = TRAMITE_CREADO
		errors['data'] = "Falta la info del trámite!"

	tramite = tramite_search (values['tramite'])

	if tramite['estatus'] != estatus:
		tramite_update_estatus (tramite, estatus)

	return result

def tramite_info (tramite_id_str):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		tramite_id = ObjectId (tramite_id_str)

		tramite = tramite_search (tramite_id)

		if (tramite is not None):
			result = json_util.dumps (tramite)

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def tramite_update_internal (tramite_id, update_values):
	error = SERVICE_ERROR_NONE

	tramite_reference = ObjectId (tramite_id)

	updated = Tramite.update (
		{
			"_id": tramite_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated tramit {tramite_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update tramit {tramite_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def tramite_update (request, tramite_id_str):
	error = SERVICE_ERROR_NONE
	errors = {}

	try:
		tramite_id = tramite_id_str.contents.str.decode ("utf-8")

		values = handle_body_input(
			request, tramite_handle_input, errors
		)

		if (not errors):
			error = tramite_update_internal(tramite_id, values)				

		else:
			cerver_log_error (b"Failed to validate tramit update input!")
			error = SERVICE_ERROR_BAD_REQUEST

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to update tramit!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors

def tramite_remove (tramite_id_str):
	error = SERVICE_ERROR_NONE

	try:
		tramite_id = tramite_id_str.contents.str.decode ("utf-8")

		values = {
			'estatus': TRAMITE_BORRADO
		}

		error = tramite_update_internal(tramite_id, values)				

		cerver_log_success (
			f"Removed tramite {tramite_id} !".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete tramite")
		error = SERVICE_ERROR_SERVER_ERROR

	return error
