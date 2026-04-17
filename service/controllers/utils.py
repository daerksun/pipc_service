from ctypes import POINTER, c_void_p
import distutils.util
import json
from typing import Any, Callable
from pprint import pprint

from cerver.http import http_query_pairs_get_value
from cerver.http import http_request_get_body

def handle_body_input (
	request: c_void_p, handle_body_input: Callable [[dict, dict], dict], errors: dict
) -> dict:
	values = None

	body_json = http_request_get_body (request)

	if (body_json is not None):
		loaded_json: dict = json.loads (body_json.contents.str)

		values = handle_body_input (loaded_json, errors)

	else:
		errors["body"] = "Request body input is required!"

	return values