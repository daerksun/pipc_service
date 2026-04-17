import os, signal, sys
import ctypes

from cerver.http import HTTP_STATUS_OK
from cerver.http import http_response_json_key_value_send

from errors import service_error_send, service_errors_send

from controllers.organizaciones import organizacion_create

# POST /api/pipc/clientes/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def organizacion_create_handler (http_receive, request):
	error, errors, organizacion_id = organizacion_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"organizacion", organizacion_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)