import datetime
from pymongoose.mongo_types import Types, Schema

class Brigada (Schema):
	schema_name = "brigadas"

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
			"brigadistas": [
					{
					"type": Types.ObjectId,
					"ref": "empleados",
					"default": None
				}
			],
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Brigada: {self.id}"