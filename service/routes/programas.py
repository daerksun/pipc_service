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

from controllers.programas import programas_read
from controllers.programas import programa_create
from controllers.programas import programa_download

from errors import SERVICE_ERROR_NONE

# GET /api/pipc/programas
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def programas_read_handler(http_receive, request):

	error, result = programas_read (request)
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

# POST /api/pipc/programas/crear
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def programa_create_handler (http_receive, request):
	error, errors, programa_id = programa_create (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"programa", programa_id.encode ("utf-8")
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)
	
# GET /api/pipc/programas/:id/descargar
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def programa_download_handler(http_receive, request):
	programa_id_str = http_request_get_param_at_idx (request, 0)

	error, result = programa_download(programa_id_str.contents.str.decode ("utf-8"))
	if (error == SERVICE_ERROR_NONE):
		actual_result = result.encode ("utf-8")
		http_response_json_custom_reference_send (
			http_receive, HTTP_STATUS_OK,
			actual_result, len (actual_result)
		)

	else:
		service_error_send (http_receive, error)

