import datetime
from pymongoose.mongo_types import Types, Schema

TRAMITE_CREADO = 0
TRAMITE_CON_BRIGADAS = 1
TRAMITE_CON_SIMULACROS = 2
TRAMITE_COMPLETO = 3
TRAMITE_IMPRESO = 4
TRAMITE_BORRADO = 5

class Tramite (Schema):
	schema_name = "tramites"

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
			"usuario": {
				"type": Types.ObjectId,
				"ref": "usuarios",
				"default": None
			},
			"titulo": {
				"type": Types.String,
				"required": True
			},
			"estatus":{
				"type": Types.Number,
				"default": 0
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Cliente: {self.id}"