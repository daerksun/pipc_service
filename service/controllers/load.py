import os
import ctypes
import json
import traceback
import hashlib
from pprint import pprint

from gridfs import GridFS
from pymongo import MongoClient

from config import MONGO_URL

from cerver.utils import cerver_log_success
from cerver.utils import cerver_log_error

from cerver.http import validate_mparts_exists
from cerver.http import validate_mparts_file

from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NONE

from models.file_info import FileInfo


def create_file(file):
	if os.path.exists(file['saved']):
		with open(file['saved'], 'rb') as binary_file:
			binary_data = binary_file.read()

	md5 = hashlib.md5(binary_data)
	file_md5 = md5.hexdigest()

	client = MongoClient (MONGO_URL)
	try:
		db = client.db
		fs = GridFS(db)
		file_id = fs.put(binary_data)
		cerver_log_success (
				f"Saved {file_id} file!".encode ("utf-8")
			)
	except:
		traceback.print_exc ()

	return file_id, file_md5	

def file_upload_handle_input (request: ctypes.c_void_p, errors: dict) -> dict:
	values = dict ()


	values["name"] = validate_mparts_exists (request, "name", errors)
	values["phone"] = validate_mparts_exists (request, "phone", errors)

	# actual file
	values["file"] = validate_mparts_file (request, "file", errors)
	if (values.get ("file")):
		values["filename"] = values["file"]["original"]
		values["file"], values["md5"] = create_file(values["file"])
		

	return values

def file_info_create_internal (values: dict) -> str:

	file_info = FileInfo (**values)

	file_info_id = file_info.save ()

	cerver_log_success (
		f"Created file info {file_info_id} db record!".encode ("utf-8")
	)

	return str(file_info_id)

def file_upload (request: ctypes.c_void_p):
	error = SERVICE_ERROR_NONE
	errors = dict ()
	result = None

	try:
		values: dict = file_upload_handle_input (request, errors)

		if (not errors):
			
			pprint(values)
			
			result = file_info_create_internal(values)

		else:
			cerver_log_error (b"Failed to validate upload report input!")
			error = SERVICE_ERROR_MISSING_VALUES

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to upload report!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error, errors, result