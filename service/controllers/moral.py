from bson import ObjectId, json_util
import ctypes
import json
import traceback
from pprint import pprint

from cerver.types import String
from cerver.utils import cerver_log_success
from cerver.utils import cerver_log_error
from cerver.utils import cerver_log_warning


from models.moral import Moral


from errors import SERVICE_ERROR_SERVER_ERROR
from errors import SERVICE_ERROR_BAD_REQUEST
from errors import SERVICE_ERROR_NONE
from errors import SERVICE_ERROR_MISSING_VALUES
from errors import SERVICE_ERROR_NOT_FOUND



def moral_create (values: dict):
	moral_id = None
	
	try:
		moral = Moral(**values)

		moral_id = str(moral.save ())

		cerver_log_success (
			f"Moral creado {moral_id} db record!".encode ("utf-8")
		)
	except:
		cerver_log_error (
			f"Not correct model".encode ("utf-8")
		)

	return moral_id

def moral_search (cliente_id):

	moral = Moral.find_one (
		{
			"cliente": cliente_id
		},
		parse=False
	)

	return moral

def moral_update (moral_id, update_values):
	error = SERVICE_ERROR_NONE

	moral_reference = ObjectId (moral_id)

	updated = Moral.update (
		{
			"_id": moral_reference
		},
		{
			"$set": update_values
		}
	)

	if (updated):
		cerver_log_success (
			f"Updated moral {moral_id} db record!".encode ("utf-8")
		)

	else:
		cerver_log_warning (
			f"Failed to update moral {moral_id} db record!".encode ("utf-8")
		)

		error = SERVICE_ERROR_BAD_REQUEST

	return error

def moral_remove (moral_id):
	error = SERVICE_ERROR_NONE

	try:
		Moral.delete ({
			"_id": moral_id
		})

		cerver_log_success (
			f"Removed moral {moral_id} db record!".encode ("utf-8")
		)

	except:
		traceback.print_exc ()
		cerver_log_error (b"Failed to delete moral!")
		error = SERVICE_ERROR_SERVER_ERROR

	return error