import datetime
from pymongoose.mongo_types import Types, Schema

class Establecimiento (Schema):
	schema_name = "establecimientos"

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
			"nombre_comercial": {
				"type": Types.String,
				"required": True
			},
			"dir_calle": {
				"type": Types.String,
				"required": True
			},
			"dir_numero": {
				"type": Types.String,
				"default": None
			},
			"dir_colonia": {
				"type": Types.String,
				"default": None
			},
			"dir_alcaldia": {
				"type": Types.String,
				"default": None
			},
			"dir_codigo_postal": {
				"type": Types.String,
				"default": 0
			},
			"lat": {
				"type": Types.Number,
				"default": 0
			},
			"long": {
				"type": Types.Number,
				"default": 0
			},
			"niveles": {
				"type": Types.String,
			},
			"sup_total": {
				"type": Types.Number,
				"default": 0
			},
			"sup_constr": {
				"type": Types.Number,
				"default": 0
			},
			"sup_en_uso": {
				"type": Types.Number,
				"default": 0
			},
			"inst_hidraulicas": {
				"type": Types.String,
			},
			"inst_electricas": {
				"type": Types.String,
			},
			"inst_especiales": {
				"type": Types.String,
			},
			"aforo": {
				"type": Types.Number,
				"default": 0
			},
			"empleados": {
				"type": Types.Number,
				"default": 0
			},
			"poblacion_flotante": {
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
		return f"Establecimiento: {self.id}"