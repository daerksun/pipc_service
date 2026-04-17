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

from controllers.clientes import clientes_read
from controllers.clientes import cliente_create
from controllers.clientes import cliente_info
from controllers.clientes import cliente_update
from controllers.clientes import cliente_remove

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/clientes
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def clientes_read_handler(http_receive, request):

	error, result = clientes_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/clientes/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def cliente_create_handler (http_receive, request):
	error, errors, cliente_id = cliente_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"cliente", cliente_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# GET /api/pipc/clientes/:id/info
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def cliente_info_handler(http_receive, request):
	cliente_id_str = http_request_get_param_at_idx (request, 0)

	error, result = cliente_info(cliente_id_str.contents.str.decode ("utf-8"))
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)
	
# PUT /api/pipc/clientes/:id/actualizar 
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def cliente_update_handler(http_receive, request):
	cliente_id_str = http_request_get_param_at_idx (request, 0)

	error, errors = cliente_update(request, cliente_id_str)

	if (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)

# DELETE /api/pipc/clientes/:id/borrar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def cliente_remove_handler (http_receive, request):
	cliente_id_str = http_request_get_param_at_idx (request, 0)

	service_error_send (http_receive, cliente_remove (cliente_id_str))

