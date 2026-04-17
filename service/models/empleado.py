import datetime
from pymongoose.mongo_types import Types, Schema

class Empleado (Schema):
	schema_name = "empleados"

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
			"nombre_completo": {
				"type": Types.String,
				"required": True
			},
			"puesto": {
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
		return f"Empleado: {self.id}"