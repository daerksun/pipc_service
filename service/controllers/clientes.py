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
from controllers.moral import moral_create
from controllers.moral import moral_search
from controllers.moral import moral_update
from controllers.moral import moral_remove


from models.cliente import Cliente

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND

def build_results_clientes(clientes):
    response = dict ()

    for cliente in clientes:
        response[str(cliente["_id"])] = cliente["razon_social"]

    return response

def clientes_read_internal(values):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		clientes = Cliente.find(
			values,
			parse=False
		)

		if (clientes):
			result = json_util.dumps(build_results_clientes(clientes))

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR
		
	return error, result

def clientes_read_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))

	return values

def clientes_read (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	result = None

	try:
		values = handle_body_input (
			request, clientes_read_handle_input, errors
		)

		if (not errors):
			error, result = clientes_read_internal (values)

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def cliente_handle_input (loaded_json: dict, errors: dict):
	values = dict ()

	values["numero_telefono"] = validate_body_value_exists (loaded_json, "numero_telefono", errors)
	values["rfc"] = validate_body_value_exists (loaded_json, "rfc", errors)
	values["giro"] = validate_body_value_exists (loaded_json, "giro", errors)
	values["correo"] = validate_body_value_exists (loaded_json, "correo", errors)
	values["tipo_identificacion"] = validate_body_value_exists (loaded_json, "tipo_identificacion", errors)
	values["numero_identificacion"] = validate_body_value_exists (loaded_json, "numero_identificacion", errors)
	values["curp"] = validate_body_value_exists (loaded_json, "curp", errors)

	values["moral"] = validate_body_value_exists (loaded_json, "moral", errors)

	if values["moral"] == True:
		moral = dict ()
		moral["apoderado_legal"] = validate_body_value_exists (loaded_json, "apoderado_legal", errors)
		moral["nacionalidad"] = validate_body_value_exists (loaded_json, "nacionalidad", errors)
		moral["acta_constitutiva"] = validate_body_value_exists (loaded_json, "acta_constitutiva", errors)
		moral["escritura"] = validate_body_value_exists (loaded_json, "escritura", errors)
		moral["notario"] = validate_body_value_exists (loaded_json, "notario", errors)

		values["moral"] = moral


	return values

def cliente_create_handle_input (loaded_json, errors: dict):
	values = dict ()

	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["razon_social"] = validate_body_value_exists (loaded_json, "razon_social", errors)

	values.update (cliente_handle_input (loaded_json, errors))

	return values

def cliente_create_validate (values: dict, errors: dict):
	result = True

	query = dict ()

	query["organizacion"] = values["organizacion"]
	query["razon_social"] = values["razon_social"]

	cliente_cursor = Cliente.find(
		query,
		parse=False
	)
	
	for cliente in cliente_cursor:
		errors["razon_social"] = "Client already exists!"
		result = False
		break
		
	return result

def cliente_create_internal (values: dict):
	cliente_id = None
	
	try:
		cliente = Cliente(**values)

		cliente_id = str(cliente.save ())

		cerver_log_success (
			f"Cliente creado {cliente_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return cliente_id

def cliente_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	cliente_id = None

	try:
		values = handle_body_input (
			request, cliente_create_handle_input, errors
		)
		
		if (not errors):
			if (cliente_create_validate (values, errors)):
				moral_values = values.pop ("moral")
				cliente_id = cliente_create_internal (values)

				if type(moral_values) is dict:
					moral_values["organizacion"] = values["organizacion"]
					moral_values["cliente"] = ObjectId (cliente_id)
					moral_create(moral_values)
	
	except:
		cerver_log_error (b"Failed to create client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, cliente_id

def cliente_search (cliente_id):
	
	cliente = Cliente.find_by_id(
		cliente_id,
		parse=False
	)

	return cliente

def cliente_info (cliente_id_str):
	error = SERVICE_ERROR_NONE
	result = None

	try:
		cliente_id = ObjectId (cliente_id_str)

		cliente = cliente_search (cliente_id)

		if (cliente is not None):
			moral = moral_search(cliente_id)

			if (moral is not None):
				cliente["moral"] = moral

			result = json_util.dumps (cliente)

		else:
			error = SERVICE_ERROR_NOT_FOUND

	except:
		traceback.print_exc ()
		error = SERVICE_ERROR_SERVER_ERROR

	return error, result

def cliente_update_internal (cliente_id, update_values):
	error = SERVICE_ERROR_NONE

	cliente_reference = ObjectId (cliente_id)

	updated = Cliente.update (
		{
			"_id": cliente_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated client {cliente_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update client {cliente_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def cliente_update (request, cliente_id_str):
	error = SERVICE_ERROR_NONE
	errors = {}

	try:
		cliente_id = cliente_id_str.contents.str.decode ("utf-8")

		values = handle_body_input(
			request, cliente_handle_input, errors
		)

		if (not errors):
			moral_values = values.pop ("moral")
			error = cliente_update_internal(cliente_id, values)

			if type(moral_values) is dict:
				moral = moral_search(ObjectId (cliente_id))

				if (moral is not None):
					error = moral_update(moral["_id"], moral_values)
				
				else:
					moral_values["organizacion"] = values["organizacion"]
					moral_values["cliente"] = ObjectId (cliente_id)
					moral_create(moral_values)
					

		else:
			cerver_log_error (b"Failed to validate client update input!")
			error = SERVICE_ERROR_BAD_REQUEST

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to update client!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors

def cliente_remove (cliente_id_str):
	error = SERVICE_ERROR_NONE

	try:
		cliente_id = ObjectId (cliente_id_str.contents.str.decode ("utf-8"))

		moral = moral_search (cliente_id)

		if (moral is not None):
			moral_remove(moral["_id"])

		Cliente.delete ({
			"_id": cliente_id
		})

		cerver_log_success (
			f"Removed cliente {cliente_id} db record!".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete cliente!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error
