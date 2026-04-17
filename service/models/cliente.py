import datetime
from pymongoose.mongo_types import Types, Schema

class Cliente (Schema):
	schema_name = "clientes"

	def __init__ (self, **kwargs):
		self.schema = {
			"organizacion": {
				"type": Types.ObjectId,
				"ref": "organizaciones",
				"default": None
			},
			"razon_social": {
				"type": Types.String,
				"required": True
			},
			"numero_telefono": {
				"type": Types.String,
				"required": True
			},
			"rfc": {
				"type": Types.String,
				"default": None
			},
			"giro": {
				"type": Types.String,
				"default": None
			},
			"correo": {
				"type": Types.String,
				"default": None
			},
			"tipo_identificacion": {
				"type": Types.String,
				"default": None
			},
			"numero_identificacion": {
				"type": Types.String,
				"default": None
			},
			"curp": {
				"type": Types.String,
				"default": None
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Cliente: {self.id}"