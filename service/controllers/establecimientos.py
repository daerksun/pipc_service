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
from cerver.http import validate_body_int_value_exists
from cerver.http import validate_body_float_value_exists
from cerver.http import validate_body_value_optional

from controllers.utils import handle_body_input

from models.establecimiento import Establecimiento

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_establecimientos(establecimientos):
    response = dict ()

    for establecimiento in establecimientos:
        response[str(establecimiento["_id"])] = establecimiento["nombre_comercial"]

    return response

def establecimientos_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		establecimientos = Establecimiento.find(
			values,
			parse=False
		)

		if (establecimientos):
			result = json_util.dumps(build_results_establecimientos(establecimientos))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def establecimientos_read_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))

	return values

def establecimientos_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, establecimientos_read_handle_input, errors
		)

		if (not errors):
			error, result = establecimientos_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to read establecimientos!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def establecimiento_handle_input (loaded_json: dict, errors: dict):
	values = {}

	values["dir_calle"] = validate_body_value_exists (loaded_json, "dir_calle", errors)
	values["dir_numero"] = validate_body_value_exists (loaded_json, "dir_numero", errors)
	values["dir_colonia"] = validate_body_value_exists (loaded_json, "dir_colonia", errors)
	values["dir_alcaldia"] = validate_body_value_exists (loaded_json, "dir_alcaldia", errors)
	values["dir_codigo_postal"] = validate_body_value_exists (loaded_json, "dir_codigo_postal", errors)
	values["lat"] = validate_body_float_value_exists (loaded_json, "lat", errors)
	values["long"] = validate_body_float_value_exists (loaded_json, "long", errors)
	values["niveles"] = validate_body_value_exists (loaded_json, "niveles", errors)
	values["sup_total"] = validate_body_float_value_exists (loaded_json, "sup_total", errors)
	values["sup_constr"] = validate_body_float_value_exists (loaded_json, "sup_constr", errors)
	values["sup_en_uso"] = validate_body_float_value_exists (loaded_json, "sup_en_uso", errors)
	values["inst_hidraulicas"] = validate_body_value_exists (loaded_json, "inst_hidraulicas", errors)
	values["inst_electricas"] = validate_body_value_exists (loaded_json, "inst_electricas", errors)
	values["inst_especiales"] = validate_body_value_exists (loaded_json, "inst_especiales", errors)
	values["aforo"] = validate_body_int_value_exists (loaded_json, "aforo", errors)
	values["empleados"] = validate_body_int_value_exists (loaded_json, "empleados", errors)
	values["poblacion_flotante"] = validate_body_int_value_exists (loaded_json, "poblacion_flotante", errors)

	return values

def establecimiento_create_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["nombre_comercial"] = validate_body_value_exists (loaded_json, "nombre_comercial", errors)

	values.update (establecimiento_handle_input (loaded_json, errors))

	pprint(values)
	return values

def establecimiento_create_validate (values: dict, errors: dict):
	result = True

	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["nombre_comercial"] = values["nombre_comercial"]

	establecimiento_cursor = Establecimiento.find(
		query,
		parse=False
	)
	
	for establecimiento in establecimiento_cursor:
		errors["nombre_comercial"] = "Store already exists!"
		result = False
		break
		
	return result

def establecimiento_create_internal (values: dict):
	error = SERVICE_ERROR_NONE
	establecimiento_id = None
	
	try:
		establecimiento = Establecimiento(**values)

		establecimiento_id = str(establecimiento.save ())

		cerver_log_success (
			f"Establecimiento creado {establecimiento_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error, establecimiento_id

def establecimiento_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	establecimiento_id = None

	try:
		values = handle_body_input (
			request, establecimiento_create_handle_input, errors
		)

		if (not errors):
			if (establecimiento_create_validate (values, errors)):
				error, establecimiento_id = establecimiento_create_internal (values)

			else:
				error = SERVICE_ERROR_BAD_REQUEST

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, establecimiento_id

def establecimiento_search(establecimiento_id):
	
	establecimiento = Establecimiento.find_by_id(
		establecimiento_id,
		parse=False
	)

	return establecimiento

def establecimiento_info (establecimiento_id_str):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		establecimiento_id = ObjectId (establecimiento_id_str)

		establecimiento = establecimiento_search(establecimiento_id)

		if (establecimiento is not None):
			result = json_util.dumps(establecimiento)

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def establecimiento_update_internal (establecimiento_id, update_values):
	error = SERVICE_ERROR_NONE

	establecimiento_reference = ObjectId (establecimiento_id)

	updated = Establecimiento.update (
		{
			"_id": establecimiento_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated establecimiento {establecimiento_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to create establecimiento {establecimiento_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def establecimiento_update (request, establecimiento_id_str):
	error = SERVICE_ERROR_NONE
	errors = {}

	try:
		establecimiento_id = establecimiento_id_str.contents.str.decode ("utf-8")

		values = handle_body_input(
			request, establecimiento_handle_input, errors
		)

		if (not errors):
			error = establecimiento_update_internal(establecimiento_id, values)

		else:
			cerver_log_error (b"Failed to validate client update input!")
			error = SERVICE_ERROR_BAD_REQUEST

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to update client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors

def establecimiento_remove (establecimiento_id_str):
	error = SERVICE_ERROR_NONE

	try:
		establecimiento_id = establecimiento_id_str.contents.str.decode ("utf-8")

		Establecimiento.delete ({
			"_id": ObjectId (establecimiento_id)
		})

		cerver_log_success (
			f"Removed establecimiento {establecimiento_id} db record!".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete establecimiento!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error
