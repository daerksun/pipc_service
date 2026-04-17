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
from controllers.tramites import tramite_correct_status

from models.programa import Programa

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_programas(programas):
    response = dict ()

    for programa in programas:
        response[str(programa["_id"])] = {
			"ruta": programa['ruta'],
			"date": str (programa['date'])
		}

    return response

def programas_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		programas = Programa.find(
			values,
			parse=False
		)

		if (programas):
			result = json_util.dumps(build_results_programas(programas))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def programas_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, programa_handle_input, errors
		)

		if (not errors):
			error, result = programas_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create programa!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def programa_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["cliente"] = ObjectId (validate_body_value_exists (loaded_json, "cliente", errors))
	values["establecimiento"] = ObjectId (validate_body_value_exists (loaded_json, "establecimiento", errors))
	values["tramite"] = ObjectId (validate_body_value_exists (loaded_json, "tramite", errors))

	return values

def programa_create_validate (values: dict):
	query = dict ()
	programa_id = None

	query["organizacion"] = values["organizacion"]
	query["cliente"] = values["cliente"]
	query["establecimiento"] = values["establecimiento"]
	query["tramite"] = values["tramite"]

	programa = Programa.find_one(
		query,
		parse=False
	)
	
	if programa:
		programa_id = str (programa['_id'])

	return programa_id

def programa_create_internal (values: dict):
	programa_id = None
	
	try:
		programa = Programa(**values)

		programa_id = str(programa.save ())

		cerver_log_success (
			f"programa creado {programa_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)
	
	return programa_id

def obtain_all_values (values):
	all_values = {}
 
	cliente_file_values (values, all_values)
	establecimiento_file_values (values, all_values)
	tramite_file_values (values, all_values)
	
	return all_values

def file_create_internal (values, programa_id):
	all_values = obtain_all_values (values)
	pprint (all_values)

def programa_generate_file (values, programa_id, errors):
	error = SERVICE_ERROR_NONE
	programa_token = None

	try:
		if (file_create_validate (programa_id, errors)):
			programa_token = file_create_internal (values, programa_id)
					
		else:
			error = SERVICE_ERROR_MISSING_VALUES
	
	except:
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, programa_token

def programa_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	programa_token = None

	try:
		values = handle_body_input (
			request, programa_handle_input, errors
		)
		
		if (not errors):
			programa_id = programa_create_validate (values)
			if (not programa_id):
				programa_id = programa_create_internal (values)
			
			if (tramite_correct_status (values, errors)):
				error, programa_token = programa_generate_file (values, programa_id, errors)
			
			else:
				error = SERVICE_ERROR_MISSING_VALUES

		else:
			error = SERVICE_ERROR_MISSING_VALUES
	
	except:
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, programa_token

# def simulacro_search (simulacro_id):
	
# 	simulacro = Simulacro.find_by_id(
# 		simulacro_id,
# 		parse=False
# 	)

# 	return simulacro

def programa_download (simulacro_id_str):
	pass
# 	error = SERVICE_ERROR_NONE
# 	result = None

# 	try:
# 		simulacro_id = ObjectId (simulacro_id_str)

# 		simulacro = simulacro_search (simulacro_id)

# 		if (simulacro is not None):
# 			result = json_util.dumps (simulacro)

# 		else:
# 			error = SERVICE_ERROR_NOT_FOUND

# 	except:
# 		traceback.print_exc ()
# 		error = SERVICE_ERROR_SERVER_ERROR

# 	return error, result

# def simulacro_update_internal (simulacro_id, update_values):
# 	error = SERVICE_ERROR_NONE

# 	simulacro_reference = ObjectId (simulacro_id)

# 	updated = Simulacro.update (
# 		{
# 			"_id": simulacro_reference
# 		},
# 		{
# 			"$set": update_values
# 		}
# 	)

# 	if (updated):
# 		cerver_log_success (
# 			f"Updated simulacro {simulacro_id} db record!".encode ("utf-8")
# 		)

# 	else:
# 		cerver_log_warning (
# 			f"Failed to update simulacro {simulacro_id} db record!".encode ("utf-8")
# 		)

# 		error = SERVICE_ERROR_BAD_REQUEST

# 	return error

# def simulacro_update (request, simulacro_id_str):
# 	error = SERVICE_ERROR_NONE
# 	errors = {}

# 	try:
# 		simulacro_id = simulacro_id_str.contents.str.decode ("utf-8")

# 		values = handle_body_input(
# 			request, simulacro_handle_input, errors
# 		)

# 		if (not errors):
# 			error = simulacro_update_internal(simulacro_id, values)				

# 		else:
# 			cerver_log_error (b"Failed to validate simulacro update input!")
# 			error = SERVICE_ERROR_BAD_REQUEST

# 	except:
# 		traceback.print_exc ()
# 		cerver_log_error (b"Failed to update simulacro!")
# 		error = SERVICE_ERROR_SERVER_ERROR

# 	return error, errors

# def simulacro_remove (simulacro_id_str):
# 	error = SERVICE_ERROR_NONE

# 	try:
# 		simulacro_id = ObjectId (simulacro_id_str.contents.str.decode ("utf-8"))

# 		Simulacro.delete ({
# 			"_id": simulacro_id
# 		})

# 		cerver_log_success (
# 			f"Removed simulacro {simulacro_id} db record!".encode ("utf-8")
# 		)

# 	except:
# 		traceback.print_exc ()
# 		cerver_log_error (b"Failed to delete simulacro!")
# 		error = SERVICE_ERROR_SERVER_ERROR

# 	return error
