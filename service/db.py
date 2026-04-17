import traceback

from pymongo import MongoClient
from pymongoose.methods import set_schemas

from config import MONGO_URL
from models.brigada import Brigada
from models.cliente import Cliente
from models.establecimiento import Establecimiento
from models.empleado import Empleado
from models.moral import Moral
from models.organizacion import Organizacion
from models.programa import Programa
from models.simulacro import Simulacro
from models.tramite import Tramite
from models.usuario import Usuario

db = None

def db_mongo_init ():
	global db

	result = False

	client = MongoClient (MONGO_URL)
	try:
		db = client.db

		db.command ("ping")

		schemas = {
			"brigadas": Brigada (empty=True).schema,
			"clientes": Cliente (empty=True).schema,
			"establecimientos": Establecimiento (empty=True).schema,
			"empleados": Empleado (empty=True).schema,
			"morales": Moral (empty=True).schema,
			"organizaciones": Organizacion (empty=True).schema,
			"programas": Programa (empty=True).schema,
			"simulacros": Simulacro (empty=True).schema,
			"tramites": Tramite (empty=True).schema,
			"usuarios": Usuario (empty=True).schema		
		}

		set_schemas (
			db, schemas,
			False
		)

		result = True

	except:
		traceback.print_exc ()

	return result
