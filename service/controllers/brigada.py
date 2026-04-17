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
from controllers.empleados import empleado_search_valid
from controllers.empleados import empleado_repetido

from models.brigada import Brigada

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_brigadas(brigadas):
    response = dict ()

    for brigada in brigadas:
        response[str(brigada["_id"])] = brigada["brigadistas"]

    return response

def brigadas_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		brigadas = Brigada.find(
			values,
			parse=False
		)

		if (brigadas):
			result = json_util.dumps(build_results_brigadas(brigadas))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def brigadas_read_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	values["tramite"] = ObjectId (validate_body_value_exists (loaded_json, "tramite", errors))

	return values

def brigadas_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, brigadas_read_handle_input, errors
		)

		if (not errors):
			error, result = brigadas_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create brigada!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def brigada_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	values["tramite"] = ObjectId (validate_body_value_exists (loaded_json, "tramite", errors))

	body_lista = validate_body_value_exists (loaded_json, "brigadistas", errors)
	lista = []
	for b in body_lista:
		lista.append (ObjectId (b))

	values["brigadistas"] = lista
	return values

def brigada_exist (values):
	result = False
	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["tramite"] = values["tramite"]

	brigada_cursor = Brigada.find_one(
		query,
		parse=False
	)
	
	if brigada_cursor:
		result = True
		
	return result


def brigada_create_validate (values: dict, errors: dict):
	result = True
	query = dict ()

	try:
		query["organizacion"] = values["organizacion"]
		query["cliente"] = values["cliente"]
		query["establecimiento"] = values["establecimiento"]
		query["tramite"] = values["tramite"]

		brigada_cursor = Brigada.find_one(
			query,
			parse=False
		)
		
		if brigada_cursor:
			errors["tramite"] = "Brigada already exists!"
			result = False

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed searching brigada")
		
	if result:
		result = brigada_empleados_validate (values, errors)

	return result

def brigada_empleados_validate (values: dict, errors: dict):
	result = True
	i = 0
	l = len (values["brigadistas"])
	for brigadista in values['brigadistas']:
		if not empleado_search_valid (brigadista, values):
			errors["brigadistas"] = "Id de empleado no encontrado!"
			result = False
			break
		if empleado_repetido (i, l, values['brigadistas']):
			errors["brigadistas"] = "Id de empleado repetido!"
			result = False
			break
		i+=1

	return result


def brigada_create_internal (values: dict):
	brigada_id = None
	
	try:
		brigada = Brigada(**values)

		brigada_id = str(brigada.save ())

		cerver_log_success (
			f"Brigada creado {brigada_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return brigada_id

def brigada_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	brigada_id = None

	try:
		values = handle_body_input (
			request, brigada_handle_input, errors
		)
		
		if (not errors):
			if (brigada_create_validate (values, errors)):
				brigada_id = brigada_create_internal (values)
			else:
				error = SERVICE_ERROR_BAD_REQUEST
	
	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create brigada")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, brigada_id


def brigada_update_internal (brigada_id, update_values: dict):
	error = SERVICE_ERROR_NONE

	brigada_reference = ObjectId (brigada_id)
	update_values.pop ("organizacion")
	update_values.pop ("cliente")
	update_values.pop ("establecimiento")
	update_values.pop ("tramite")
	pprint (update_values)
	updated = Brigada.update (
		{
			"_id": brigada_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated brigada {brigada_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update brigada {brigada_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def brigada_update (request, brigada_id_str):
	error = SERVICE_ERROR_NONE
	errors = {}

	try:
		brigada_id = brigada_id_str.contents.str.decode ("utf-8")

		values = handle_body_input(
			request, brigada_handle_input, errors
		)

		if (not errors):
			if (brigada_empleados_validate (values, errors)):
				error = brigada_update_internal(brigada_id, values)
			else:
				error = SERVICE_ERROR_BAD_REQUEST

		else:
			cerver_log_error (b"Failed to validate brigadaupdate input!")
			error = SERVICE_ERROR_BAD_REQUEST

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to update brigada")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors

def brigada_remove (brigada_id_str):
	error = SERVICE_ERROR_NONE

	try:
		brigada_id = ObjectId (brigada_id_str.contents.str.decode ("utf-8"))

		Brigada.delete ({
			"_id": brigada_id
		})

		cerver_log_success (
			f"Removed brigada {brigada_id} db record!".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete brigada!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error
