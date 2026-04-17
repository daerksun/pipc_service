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

from controllers.tramites import tramites_read
from controllers.tramites import tramite_create
from controllers.tramites import tramite_info
from controllers.tramites import tramite_update
from controllers.tramites import tramite_remove

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/tramites
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def tramites_read_handler(http_receive, request):

	error, result = tramites_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/tramites/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def tramite_create_handler (http_receive, request):
	error, errors, tramite_id = tramite_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"tramite", tramite_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# GET /api/pipc/tramites/:id/info
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def tramite_info_handler(http_receive, request):
	tramite_id_str = http_request_get_param_at_idx (request, 0)

	error, result = tramite_info(tramite_id_str.contents.str.decode ("utf-8"))
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)
	
# PUT /api/pipc/tramites/:id/actualizar 
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def tramite_update_handler(http_receive, request):
	tramite_id_str = http_request_get_param_at_idx (request, 0)

	error, errors = tramite_update(request, tramite_id_str)

	if (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)

# DELETE /api/pipc/tramites/:id/borrar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def tramite_remove_handler (http_receive, request):
	tramite_id_str = http_request_get_param_at_idx (request, 0)

	service_error_send (http_receive, tramite_remove (tramite_id_str))

