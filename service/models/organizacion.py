import datetime
from pymongoose.mongo_types import Types, Schema

class Organizacion (Schema):
	schema_name = "organizaciones"

	def __init__ (self, **kwargs):
		self.schema = {
			"nombre": {
				"type": Types.String,
				"required": True
			},
			"estado": {
				"type": Types.String,
				"required": True
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Establecimiento: {self.id}"