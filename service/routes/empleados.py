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

from controllers.empleados import empleados_read
from controllers.empleados import empleado_create
from controllers.empleados import empleado_info
from controllers.empleados import empleado_update
from controllers.empleados import empleado_remove

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/empleados
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def empleados_read_handler(http_receive, request):

	error, result = empleados_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/empleados/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def empleado_create_handler (http_receive, request):
	error, errors, empleado_id = empleado_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"empleado", empleado_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# GET /api/pipc/empleados/:id/info
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def empleado_info_handler(http_receive, request):
	empleado_id_str = http_request_get_param_at_idx (request, 0)

	error, result = empleado_info(empleado_id_str.contents.str.decode ("utf-8"))
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)
	
# PUT /api/pipc/empleados/:id/actualizar 
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def empleado_update_handler(http_receive, request):
	empleado_id_str = http_request_get_param_at_idx (request, 0)

	error, errors = empleado_update(request, empleado_id_str)

	if (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)

# DELETE /api/pipc/empleados/:id/borrar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def empleado_remove_handler (http_receive, request):
	empleado_id_str = http_request_get_param_at_idx (request, 0)

	service_error_send (http_receive, empleado_remove (empleado_id_str))

