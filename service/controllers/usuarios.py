from bson import ObjectId, json_util
import ctypes
import json
import traceback
from pprint import pprint

from cerver.types import String
from cerver.utils import cerver_log_success
from cerver.utils import cerver_log_error

from cerver.http import validate_body_value_exists
from cerver.http import validate_body_value_optional
from cerver.http import validate_body_int_value_exists

from controllers.utils import handle_body_input

from models.usuario import Usuario

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES


def usuario_create_handle_input (loaded_json, errors: dict):
	values = dict ()
	
	values["organizacion"] = ObjectId (validate_body_value_exists (loaded_json, "organizacion", errors))
	values["nombre"] = validate_body_value_exists (loaded_json, "nombre", errors)
	values["contraseña"] = validate_body_value_exists (loaded_json, "contraseña", errors)

	return values

def usuario_create_validate (values: dict, errors: dict):
	result = True

	usuario_cursor = Usuario.find (
		values,
		parse=False
	)
	
	for usuario in usuario_cursor:
		errors["values"] = "Usuario already exists!"
		result = False
		break
		
	return result

def usuario_create_internal (values: dict):
	usuario_id = None
	
	try:
		usuario = Usuario (**values)

		usuario_id = str (usuario.save ())

		cerver_log_success (
			f"Usuario creado {usuario_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return usuario_id

def usuario_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	usuario_id = None

	try:
		values = handle_body_input (
			request, usuario_create_handle_input, errors
		)

		if (not errors):
			if (usuario_create_validate (values, errors)):
				usuario_id = usuario_create_internal (values)

			else:
				error = SERVICE_ERROR_BAD_REQUEST

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create usuario")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, usuario_id
