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

from models.organizacion import Organizacion

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES


def organizacion_create_handle_input (loaded_json, errors: dict):
	values = dict ()
	
	values["nombre"] = validate_body_value_exists (loaded_json, "nombre", errors)
	values["estado"] = validate_body_value_exists (loaded_json, "estado", errors)

	return values

def organizacion_create_validate (values: dict, errors: dict):
	result = True

	organizacion_cursor = Organizacion.find (
		values,
		parse=False
	)
	
	for organizacion in organizacion_cursor:
		errors["values"] = "Organization already exists!"
		result = False
		break
		
	return result

def organizacion_create_internal (values: dict):
	organizacion_id = None
	
	try:
		organizacion = Organizacion (**values)

		organizacion_id = str (organizacion.save ())

		cerver_log_success (
			f"Organizacion creada {organizacion_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return organizacion_id

def organizacion_create (request):
	error = SERVICE_ERROR_NONE
	errors = {}
	organizacion_id = None

	try:
		values = handle_body_input (
			request, organizacion_create_handle_input, errors
		)

		if (not errors):
			if (organizacion_create_validate (values, errors)):
				organizacion_id = organizacion_create_internal (values)

			else:
				error = SERVICE_ERROR_BAD_REQUEST

		else:
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to create organizacion")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, organizacion_id
