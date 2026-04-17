import datetime
from pymongoose.mongo_types import Types, Schema

class Usuario (Schema):
	schema_name = "usuarios"

	def __init__ (self, **kwargs):
		self.schema = {
			"organizacion": {
				"type": Types.ObjectId,
				"ref": "organizaciones",
				"default": None
			},
			"nombre": {
				"type": Types.String,
				"required": True
			},
			"contraseña": {
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