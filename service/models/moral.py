import datetime
from pymongoose.mongo_types import Types, Schema

class Moral (Schema):
	schema_name = "morales"

	def __init__ (self, **kwargs):
		self.schema = {
			"organizacion": {
				"type": Types.ObjectId,
				"ref": "organizaciones",
				"default": None
			},
			"cliente": {
				"type": Types.ObjectId,
				"ref": "clientes",
				"default": None
			},
			"apoderado_legal": {
				"type": Types.String,
				"required": True
			},
			"nacionalidad": {
				"type": Types.String,
				"required": True
			},
			"acta_constitutiva": {
				"type": Types.String,
				"default": 0
			},
			"escritura": {
				"type": Types.String,
				"default": 0
			},
			"notario": {
				"type": Types.String,
				"default": 0
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Regimen Moral: {self.id}"