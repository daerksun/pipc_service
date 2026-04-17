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

from controllers.brigada import brigadas_read
from controllers.brigada import brigada_create
from controllers.brigada import brigada_update
from controllers.brigada import brigada_remove

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/brigadas
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def brigadas_read_handler(http_receive, request):

	error, result = brigadas_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/brigadas/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def brigada_create_handler (http_receive, request):
	error, errors, brigada_id = brigada_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"brigada", brigada_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# PUT /api/pipc/brigadas/:id/actualizar 
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def brigada_update_handler(http_receive, request):
	brigada_id_str = http_request_get_param_at_idx (request, 0)

	error, errors = brigada_update(request, brigada_id_str)

	if (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)

# DELETE /api/pipc/brigadas/:id/borrar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def brigada_remove_handler (http_receive, request):
	brigada_id_str = http_request_get_param_at_idx (request, 0)

	service_error_send (http_receive, brigada_remove (brigada_id_str))

