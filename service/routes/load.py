import ctypes

from cerver import *
from cerver.http import *

from errors import service_error_send, service_errors_send

from controllers.load import file_upload


# POST /api/files/upload
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def load_handler (http_receive, request):
	error, errors, file_info = file_upload (request)

	if (not error):
		http_response_json_key_value_send (
			http_receive, HTTP_STATUS_OK,
			b"file_info", file_info.encode ("utf-8")
		)

		http_response_send_file (
			
		)

	elif (errors):
		service_errors_send (http_receive, error, errors)

	else:
		service_error_send (http_receive, error)