from bson import ObjectId, json_util
import ctypes
import datetime
import json
import traceback
from pprint import pprint

from cerver.types import String
from cerver.utils import cerver_log_success
from cerver.utils import cerver_log_error
from cerver.utils import cerver_log_warning

from cerver.http import validate_body_value_exists

from controllers.utils import handle_body_input

from models.simulacro import Simulacro

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_simulacros(simulacros):
    response = dict ()

    for simulacro in simulacros:
        response[str(simulacro["_id"])] = {
			"tema": simulacro['tema'],
			"instructor": simulacro['instructor'],
			"aplicacion": simulacro['aplicacion']
		}

    return response

def simulacros_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		simulacros = Simulacro.find(
			values,
			parse=False
		)

		if (simulacros):
			result = json_util.dumps(build_results_simulacros(simulacros))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def simulacros_read_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	values["tramite"] = ObjectId (validate_body_value_exists (loaded_json, "tramite", errors))


	return values

def simulacros_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, simulacros_read_handle_input, errors
		)

		if (not errors):
			error, result = simulacros_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create simulacro!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def simulacro_handle_input (loaded_json: dict, errors: dict):
	values = dict ()

	values["instructor"] = validate_body_value_exists (loaded_json, "instructor", errors)
	values["aplicacion"] = datetime.datetime.strptime (validate_body_value_exists (loaded_json, "aplicacion", errors), "%d/%m/%y %H:%M:%S")

	return values

def simulacro_create_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	values["tramite"] = ObjectId (validate_body_value_exists (loaded_json, "tramite", errors))
	values["tema"] = validate_body_value_exists (loaded_json, "tema", errors)
	
	values.update (simulacro_handle_input (loaded_json, errors))
	
	return values

def simulacros_exist (values):
	result = False
	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["tramite"] = values["tramite"]

	simulacros_cursor = Simulacro.find(
		query,
		parse=False
	)
	
	if len (list (simulacros_cursor)) > 3:
		result = True
		
	return result

def simulacro_create_validate (values: dict, errors: dict):
	result = True

	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["tramite"] = values["tramite"]
	query["tema"] = values["tema"]

	simulacro_cursor = Simulacro.find(
		query,
		parse=False
	)
	
	for simulacro in simulacro_cursor:
		errors["tema"] = "simulacro already exists!"
		result = False
		break
		
	return result

def simulacro_create_internal (values: dict):
	simulacro_id = None
	
	try:
		simulacro = Simulacro(**values)

		simulacro_id = str(simulacro.save ())

		cerver_log_success (
			f"simulacro creado {simulacro_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return simulacro_id

def simulacro_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	simulacro_id = None

	try:
		values = handle_body_input (
			request, simulacro_create_handle_input, errors
		)
		
		if (not errors):
			if (simulacro_create_validate (values, errors)):
				simulacro_id = simulacro_create_internal (values)
			else:
				error = SERVICE_ERROR_BAD_REQUEST
		else:
			error = SERVICE_ERROR_MISSING_VALUES
	
	except:
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, simulacro_id

def simulacro_search (simulacro_id):
	
	simulacro = Simulacro.find_by_id(
		simulacro_id,
		parse=False
	)

	return simulacro

def simulacro_info (simulacro_id_str):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		simulacro_id = ObjectId (simulacro_id_str)

		simulacro = simulacro_search (simulacro_id)

		if (simulacro is not None):
			result = json_util.dumps (simulacro)

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def simulacro_update_internal (simulacro_id, update_values):
	error = SERVICE_ERROR_NONE

	simulacro_reference = ObjectId (simulacro_id)

	updated = Simulacro.update (
		{
			"_id": simulacro_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated simulacro {simulacro_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update simulacro {simulacro_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def simulacro_update (request, simulacro_id_str):
	error = SERVICE_ERROR_NONE
	errors = {}

	try:
		simulacro_id = simulacro_id_str.contents.str.decode ("utf-8")

		values = handle_body_input(
			request, simulacro_handle_input, errors
		)

		if (not errors):
			error = simulacro_update_internal(simulacro_id, values)				

		else:
			cerver_log_error (b"Failed to validate simulacro update input!")
			error = SERVICE_ERROR_BAD_REQUEST

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to update simulacro!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors

def simulacro_remove (simulacro_id_str):
	error = SERVICE_ERROR_NONE

	try:
		simulacro_id = ObjectId (simulacro_id_str.contents.str.decode ("utf-8"))

		Simulacro.delete ({
			"_id": simulacro_id
		})

		cerver_log_success (
			f"Removed simulacro {simulacro_id} db record!".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete simulacro!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error
