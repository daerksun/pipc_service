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

from models.empleado import Empleado

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_empleados(empleados):
    response = dict ()

    for empleado in empleados:
        response[str(empleado["_id"])] = {
			"nombre_completo": empleado['nombre_completo'],
			"puesto": empleado['puesto']
		}

    return response

def empleados_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		empleados = Empleado.find(
			values,
			parse=False
		)

		if (empleados):
			result = json_util.dumps(build_results_empleados(empleados))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def empleados_read_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))

	return values

def empleados_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, empleados_read_handle_input, errors
		)

		if (not errors):
			error, result = empleados_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def empleado_handle_input (loaded_json: dict, errors: dict):
	values = dict ()

	values["puesto"] = validate_body_value_exists (loaded_json, "puesto", errors)
	values["nombre_completo"] = validate_body_value_exists (loaded_json, "nombre_completo", errors)

	return values

def empleado_create_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	
	values.update (empleado_handle_input (loaded_json, errors))

	return values

def empleado_create_validate (values: dict, errors: dict):
	result = True

	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["nombre_completo"] = values["nombre_completo"]

	empleado_cursor = Empleado.find(
		query,
		parse=False
	)
	
	for empleado in empleado_cursor:
		errors["nombre_completo"] = "Empleado already exists!"
		result = False
		break
		
	return result

def empleado_create_internal (values: dict):
	empleado_id = None
	
	try:
		empleado = Empleado(**values)

		empleado_id = str(empleado.save ())

		cerver_log_success (
			f"Empleado creado {empleado_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return empleado_id

def empleado_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	empleado_id = None

	try:
		values = handle_body_input (
			request, empleado_create_handle_input, errors
		)
		
		if (not errors):
			if (empleado_create_validate (values, errors)):
				empleado_id = empleado_create_internal (values)
	
	except:
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, empleado_id

def empleado_search (empleado_id):
	
	empleado = Empleado.find_by_id(
		empleado_id,
		parse=False
	)

	return empleado

def empleado_search_valid (empleado_id, values: dict):
	result = None

	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["_id"] = empleado_id

	empleado_cursor = Empleado.find(
		query,
		parse=False
	)
	
	for empleado in empleado_cursor:
		result = empleado
		break
		
	return result

def empleado_repetido (i, l, brigadistas):
	result = False

	s = i + 1
	while s < l:
		if brigadistas[i] == brigadistas[s]:
			result = True
			break
		s += 1

	return result

def empleado_info (empleado_id_str):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		empleado_id = ObjectId (empleado_id_str)

		empleado = empleado_search (empleado_id)

		if (empleado is not None):
			result = json_util.dumps (empleado)

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def empleado_update_internal (empleado_id, update_values):
	error = SERVICE_ERROR_NONE

	empleado_reference = ObjectId (empleado_id)

	updated = Empleado.update (
		{
			"_id": empleado_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated empleado {empleado_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update empleado {empleado_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def empleado_update (request, empleado_id_str):
	error = SERVICE_ERROR_NONE
	errors = {}

	try:
		empleado_id = empleado_id_str.contents.str.decode ("utf-8")

		values = handle_body_input(
			request, empleado_handle_input, errors
		)

		if (not errors):
			error = empleado_update_internal(empleado_id, values)				

		else:
			cerver_log_error (b"Failed to validate empleado update input!")
			error = SERVICE_ERROR_BAD_REQUEST

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to update empleado!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors

def empleado_remove (empleado_id_str):
	error = SERVICE_ERROR_NONE

	try:
		empleado_id = ObjectId (empleado_id_str.contents.str.decode ("utf-8"))

		Empleado.delete ({
			"_id": empleado_id
		})

		cerver_log_success (
			f"Removed empleado {empleado_id} db record!".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete empleado!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error
