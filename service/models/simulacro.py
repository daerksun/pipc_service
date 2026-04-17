import datetime
from pymongoose.mongo_types import Types, Schema

class Simulacro (Schema):
	schema_name = "simulacros"

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
			"establecimiento": {
				"type": Types.ObjectId,
				"ref": "establecimientos",
				"default": None
			},
			"tramite": {
				"type": Types.ObjectId,
				"ref": "tramites",
				"default": None
			},
			"tema": {
				"type": Types.String,
				"required": True
			},
			"instructor": {
				"type": Types.String,
				"required": True
			},
			"aplicacion": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Simulacro: {self.id}"