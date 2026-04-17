import os, signal, sys
import ctypes

from cerver.http import HTTP_STATUS_OK
from cerver.http import http_response_json_custom_reference_send
from cerver.http import http_response_json_key_value_send
from cerver.http import http_request_get_param_at_idx
from cerver.http import http_request_get_body
from cerver.http import http_request_get_query_params
from cerver.http import http_request_get_query_value

from errors import service_error_send, service_errors_send

from controllers.simulacros import simulacros_read
from controllers.simulacros import simulacro_create
from controllers.simulacros import simulacro_info
from controllers.simulacros import simulacro_update
from controllers.simulacros import simulacro_remove

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/simulacros
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def simulacros_read_handler(http_receive, request):

	error, result = simulacros_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/simulacros/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def simulacro_create_handler (http_receive, request):
	error, errors, simulacro_id = simulacro_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"simulacro", simulacro_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# GET /api/pipc/simulacros/:id/info
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def simulacro_info_handler(http_receive, request):
	simulacro_id_str = http_request_get_param_at_idx (request, 0)

	error, result = simulacro_info(simulacro_id_str.contents.str.decode ("utf-8"))
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)
	
# PUT /api/pipc/simulacros/:id/actualizar 
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def simulacro_update_handler(http_receive, request):
	simulacro_id_str = http_request_get_param_at_idx (request, 0)

	error, errors = simulacro_update(request, simulacro_id_str)

	if (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)

# DELETE /api/pipc/simulacros/:id/borrar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def simulacro_remove_handler (http_receive, request):
	simulacro_id_str = http_request_get_param_at_idx (request, 0)

	service_error_send (http_receive, simulacro_remove (simulacro_id_str))

