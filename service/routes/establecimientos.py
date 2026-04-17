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

from controllers.establecimientos import establecimientos_read
from controllers.establecimientos import establecimiento_create
from controllers.establecimientos import establecimiento_info
from controllers.establecimientos import establecimiento_update
from controllers.establecimientos import establecimiento_remove

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/establecimientos
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def establecimientos_read_handler(http_receive, request):

	error, result = establecimientos_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/establecimientos/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def establecimiento_create_handler (http_receive, request):
	error, errors, establecimiento_id = establecimiento_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"establecimiento", establecimiento_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# GET /api/pipc/establecimientos/:id/info
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def establecimiento_info_handler(http_receive, request):
	establecimiento_id_str = http_request_get_param_at_idx (request, 0)

	error, result = establecimiento_info(establecimiento_id_str.contents.str.decode ("utf-8"))
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)
	
# PUT /api/pipc/establecimientos/:id/actualizar 
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def establecimiento_update_handler(http_receive, request):
	establecimiento_id_str = http_request_get_param_at_idx (request, 0)

	error, errors = establecimiento_update(request, establecimiento_id_str)

	if (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)

# DELETE /api/pipc/establecimientos/:id/borrar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def establecimiento_remove_handler (http_receive, request):
	establecimiento_id_str = http_request_get_param_at_idx (request, 0)

	service_error_send (http_receive, establecimiento_remove (establecimiento_id_str))

