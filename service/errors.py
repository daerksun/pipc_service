import ctypes
import json

from cerver.http import HTTP_STATUS_OK
from cerver.http import HTTP_STATUS_BAD_REQUEST
from cerver.http import HTTP_STATUS_UNAUTHORIZED
from cerver.http import HTTP_STATUS_NOT_FOUND
from cerver.http import HTTP_STATUS_INTERNAL_SERVER_ERROR
from cerver.http import http_response_json_key_value
from cerver.http import http_response_send
from cerver.http import http_response_render_json
from cerver.http import http_response_delete

SERVICE_ERROR_NONE = 0
SERVICE_ERROR_BAD_REQUEST = 1
SERVICE_ERROR_MISSING_VALUES = 2
SERVICE_ERROR_BAD_USER = 3
SERVICE_ERROR_UNAUTHORIZED = 4
SERVICE_ERROR_NOT_FOUND = 5
SERVICE_ERROR_SERVER_ERROR = 6

none_error = http_response_json_key_value (
	HTTP_STATUS_OK, b"oki", b"doki"
)

bad_request_error = http_response_json_key_value (
	HTTP_STATUS_BAD_REQUEST, b"error", b"Bad request!"
)

missing_values = http_response_json_key_value (
	HTTP_STATUS_BAD_REQUEST, b"error", b"Missing values!"
)

bad_user_error = http_response_json_key_value (
	HTTP_STATUS_BAD_REQUEST, b"error", b"Bad user!"
)

failed_auth_error = http_response_json_key_value (
	HTTP_STATUS_UNAUTHORIZED, b"error", b"Failed authentication!"
)

not_found_error = http_response_json_key_value (
	HTTP_STATUS_NOT_FOUND, b"error", b"Not found!"
)

server_error = http_response_json_key_value (
	HTTP_STATUS_INTERNAL_SERVER_ERROR,
	b"error", b"Server error!"
)

def service_error_get_status (service_error: int):
	result = None

	if (service_error == SERVICE_ERROR_NONE):
		result = HTTP_STATUS_OK

	elif (service_error == SERVICE_ERROR_BAD_REQUEST):
		result = HTTP_STATUS_BAD_REQUEST

	elif (service_error == SERVICE_ERROR_MISSING_VALUES):
		result = HTTP_STATUS_BAD_REQUEST

	elif (service_error == SERVICE_ERROR_BAD_USER):
		result = HTTP_STATUS_BAD_REQUEST

	elif (service_error == SERVICE_ERROR_UNAUTHORIZED):
		result = HTTP_STATUS_UNAUTHORIZED

	elif (service_error == SERVICE_ERROR_NOT_FOUND):
		result = HTTP_STATUS_NOT_FOUND

	elif (service_error == SERVICE_ERROR_SERVER_ERROR):
		result = HTTP_STATUS_INTERNAL_SERVER_ERROR

	return result

def service_error_send (http_receive: ctypes.c_void_p, service_error: int):
	if (service_error == SERVICE_ERROR_NONE):
		http_response_send (none_error, http_receive)

	elif (service_error == SERVICE_ERROR_BAD_REQUEST):
		http_response_send (bad_request_error, http_receive)

	elif (service_error == SERVICE_ERROR_MISSING_VALUES):
		http_response_send (missing_values, http_receive)

	elif (service_error == SERVICE_ERROR_BAD_USER):
		http_response_send (bad_user_error, http_receive)

	elif (service_error == SERVICE_ERROR_UNAUTHORIZED):
		http_response_send (failed_auth_error, http_receive)

	elif (service_error == SERVICE_ERROR_NOT_FOUND):
		http_response_send (not_found_error, http_receive)

	elif (service_error == SERVICE_ERROR_SERVER_ERROR):
		http_response_send (server_error, http_receive)

def service_errors_send (
	http_receive: ctypes.c_void_p, service_error: int, errors: dict
):
	json_errors = json.dumps (errors).encode ("utf-8")

	http_response_render_json (
		http_receive, service_error_get_status (service_error),
		json_errors, len (json_errors)
	)

def service_errors_end ():
	http_response_delete (bad_request_error)
	http_response_delete (missing_values)
	http_response_delete (bad_user_error)
	http_response_delete (failed_auth_error)
	http_response_delete (not_found_error)
	http_response_delete (server_error)
