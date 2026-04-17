import signal, sys
import ctypes

from cerver import *
from cerver.http import *

from db import db_mongo_init

# from routes.load import load_handler
from routes.organizaciones import organizacion_create_handler
from routes.usuarios import usuario_create_handler
from routes.clientes import clientes_read_handler
from routes.clientes import cliente_info_handler
from routes.clientes import cliente_create_handler
from routes.clientes import cliente_update_handler
from routes.clientes import cliente_remove_handler
from routes.establecimientos import establecimientos_read_handler
from routes.establecimientos import establecimiento_create_handler
from routes.establecimientos import establecimiento_info_handler
from routes.establecimientos import establecimiento_update_handler
from routes.establecimientos import establecimiento_remove_handler
from routes.tramites import tramites_read_handler
from routes.tramites import tramite_create_handler
from routes.tramites import tramite_info_handler
from routes.tramites import tramite_update_handler
from routes.tramites import tramite_remove_handler
from routes.brigada import brigadas_read_handler
from routes.brigada import brigada_create_handler
from routes.brigada import brigada_update_handler
from routes.brigada import brigada_remove_handler
from routes.simulacros import simulacros_read_handler
from routes.simulacros import simulacro_create_handler
from routes.simulacros import simulacro_info_handler
from routes.simulacros import simulacro_update_handler
from routes.simulacros import simulacro_remove_handler
from routes.empleados import empleados_read_handler
from routes.empleados import empleado_create_handler
from routes.empleados import empleado_info_handler
from routes.empleados import empleado_update_handler
from routes.empleados import empleado_remove_handler
from routes.programas import programas_read_handler
from routes.programas import programa_create_handler
from routes.programas import programa_download_handler


web_service = None

# end
def end (signum, frame):
	# cerver_stats_print (web_service, False, False)
	http_cerver_all_stats_print (http_cerver_get (web_service))
	cerver_teardown (web_service)
	cerver_end ()
	sys.exit ("Done!")

# GET /
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def main_handler (http_receive, request):
	http_response_send_file (
		http_receive, HTTP_STATUS_OK,
		b"./examples/http/public/index.html"
	)

def set_organizaciones_routes(main_route):
	# POST /api/pipc/organizaciones/crear
	organizacion_create_route = http_route_create (REQUEST_METHOD_POST, b"organizacion/crear", organizacion_create_handler)
	http_route_child_add (main_route, organizacion_create_route)

def set_usuarios_routes(main_route):
	# POST /api/pipc/usuario/crear
	usuario_create_route = http_route_create (REQUEST_METHOD_POST, b"usuario/crear", usuario_create_handler)
	http_route_child_add (main_route, usuario_create_route)



def set_clientes_routes(main_route):
	# GET /api/pipc/clientes
	clientes_route = http_route_create (REQUEST_METHOD_GET, b"clientes", clientes_read_handler)
	http_route_child_add (main_route, clientes_route)

	# POST /api/pipc/clientes/crear
	cliente_create_route = http_route_create (REQUEST_METHOD_POST, b"clientes/crear", cliente_create_handler)
	http_route_child_add (main_route, cliente_create_route)

	# GET /api/pipc/clientes/:id/info
	cliente_info_route = http_route_create (REQUEST_METHOD_GET, b"clientes/:id/info", cliente_info_handler)
	http_route_child_add (main_route, cliente_info_route)

	# PUT /api/pipc/clientes/:id/actualizar
	cliente_update_route = http_route_create (REQUEST_METHOD_PUT, b"clientes/:id/actualizar", cliente_update_handler)
	http_route_child_add (main_route, cliente_update_route)

	# DELETE /api/pipc/clientes/:id/borrar
	cliente_delete_route = http_route_create (REQUEST_METHOD_DELETE, b"clientes/:id/borrar", cliente_remove_handler)
	http_route_child_add (main_route, cliente_delete_route)


def set_establecimientos_routes(main_route):
	# GET /api/pipc/establecimientos
	establecimientos_route = http_route_create (REQUEST_METHOD_GET, b"establecimientos", establecimientos_read_handler)
	http_route_child_add (main_route, establecimientos_route)

	# POST /api/pipc/establecimientos/crear
	establecimiento_create_route = http_route_create (REQUEST_METHOD_POST, b"establecimientos/crear", establecimiento_create_handler)
	http_route_child_add (main_route, establecimiento_create_route)

	# GET /api/pipc/establecimientos/:id/info
	establecimiento_info_route = http_route_create (REQUEST_METHOD_GET, b"establecimientos/:id/info", establecimiento_info_handler)
	http_route_child_add (main_route, establecimiento_info_route)

	# PUT /api/pipc/establecimientos/:id/actualizar
	establecimiento_update_route = http_route_create (REQUEST_METHOD_PUT, b"establecimientos/:id/actualizar", establecimiento_update_handler)
	http_route_child_add (main_route, establecimiento_update_route)

	# DELETE /api/pipc/establecimientos/:id/borrar
	establecimiento_delete_route = http_route_create (REQUEST_METHOD_DELETE, b"establecimientos/:id/borrar", establecimiento_remove_handler)
	http_route_child_add (main_route, establecimiento_delete_route)


def set_tramites_routes(main_route):
	# GET /api/pipc/tramites
	tramites_route = http_route_create (REQUEST_METHOD_GET, b"tramites", tramites_read_handler)
	http_route_child_add (main_route, tramites_route)

	# POST /api/pipc/tramites/crear
	tramite_create_route = http_route_create (REQUEST_METHOD_POST, b"tramites/crear", tramite_create_handler)
	http_route_child_add (main_route, tramite_create_route)

	# GET /api/pipc/tramites/:id/info
	tramite_info_route = http_route_create (REQUEST_METHOD_GET, b"tramites/:id/info", tramite_info_handler)
	http_route_child_add (main_route, tramite_info_route)

	# PUT /api/pipc/tramites/:id/actualizar
	tramite_update_route = http_route_create (REQUEST_METHOD_PUT, b"tramites/:id/actualizar", tramite_update_handler)
	http_route_child_add (main_route, tramite_update_route)

	# DELETE /api/pipc/tramites/:id/borrar
	tramite_delete_route = http_route_create (REQUEST_METHOD_DELETE, b"tramites/:id/borrar", tramite_remove_handler)
	http_route_child_add (main_route, tramite_delete_route)

def set_brigadas_routes(main_route):
	# GET /api/pipc/brigadas
	brigadas_route = http_route_create (REQUEST_METHOD_GET, b"brigadas", brigadas_read_handler)
	http_route_child_add (main_route, brigadas_route)

	# POST /api/pipc/brigadas/crear
	brigada_create_route = http_route_create (REQUEST_METHOD_POST, b"brigadas/crear", brigada_create_handler)
	http_route_child_add (main_route, brigada_create_route)

	# PUT /api/pipc/brigadas/:id/actualizar
	brigada_update_route = http_route_create (REQUEST_METHOD_PUT, b"brigadas/:id/actualizar", brigada_update_handler)
	http_route_child_add (main_route, brigada_update_route)

	# DELETE /api/pipc/brigadas/:id/borrar
	brigada_delete_route = http_route_create (REQUEST_METHOD_DELETE, b"brigadas/:id/borrar", brigada_remove_handler)
	http_route_child_add (main_route, brigada_delete_route)

def set_simulacros_routes(main_route):
	# GET /api/pipc/simulacros
	simulacros_route = http_route_create (REQUEST_METHOD_GET, b"simulacros", simulacros_read_handler)
	http_route_child_add (main_route, simulacros_route)

	# POST /api/pipc/simulacros/crear
	simulacro_create_route = http_route_create (REQUEST_METHOD_POST, b"simulacros/crear", simulacro_create_handler)
	http_route_child_add (main_route, simulacro_create_route)

	# GET /api/pipc/simulacros/:id/info
	simulacro_info_route = http_route_create (REQUEST_METHOD_GET, b"simulacros/:id/info", simulacro_info_handler)
	http_route_child_add (main_route, simulacro_info_route)

	# PUT /api/pipc/simulacros/:id/actualizar
	simulacro_update_route = http_route_create (REQUEST_METHOD_PUT, b"simulacros/:id/actualizar", simulacro_update_handler)
	http_route_child_add (main_route, simulacro_update_route)

	# DELETE /api/pipc/simulacros/:id/borrar
	simulacro_delete_route = http_route_create (REQUEST_METHOD_DELETE, b"simulacros/:id/borrar", simulacro_remove_handler)
	http_route_child_add (main_route, simulacro_delete_route)

def set_empleados_routes(main_route):
	# GET /api/pipc/empleados
	empleados_route = http_route_create (REQUEST_METHOD_GET, b"empleados", empleados_read_handler)
	http_route_child_add (main_route, empleados_route)

	# POST /api/pipc/empleados/crear
	empleado_create_route = http_route_create (REQUEST_METHOD_POST, b"empleados/crear", empleado_create_handler)
	http_route_child_add (main_route, empleado_create_route)

	# GET /api/pipc/empleados/:id/info
	empleado_info_route = http_route_create (REQUEST_METHOD_GET, b"empleados/:id/info", empleado_info_handler)
	http_route_child_add (main_route, empleado_info_route)

	# PUT /api/pipc/empleados/:id/actualizar
	empleado_update_route = http_route_create (REQUEST_METHOD_PUT, b"empleados/:id/actualizar", empleado_update_handler)
	http_route_child_add (main_route, empleado_update_route)

	# DELETE /api/pipc/empleados/:id/borrar
	empleado_delete_route = http_route_create (REQUEST_METHOD_DELETE, b"empleados/:id/borrar", empleado_remove_handler)
	http_route_child_add (main_route, empleado_delete_route)

def set_programas_routes(main_route):
	# GET /api/pipc/programas
	programas_route = http_route_create (REQUEST_METHOD_GET, b"programas", programas_read_handler)
	http_route_child_add (main_route, programas_route)

	# POST /api/pipc/programas/crear
	programa_create_route = http_route_create (REQUEST_METHOD_POST, b"programas/crear", programa_create_handler)
	http_route_child_add (main_route, programa_create_route)

	# GET /api/pipc/programas/:id/descargar
	programa_download_route = http_route_create (REQUEST_METHOD_GET, b"programas/:id/descargar", programa_download_handler)
	http_route_child_add (main_route, programa_download_route)



	# # POST /api/files/load
	# load_route = http_route_create (REQUEST_METHOD_POST, b"load", load_handler)
	# http_route_set_modifier (load_route, HTTP_ROUTE_MODIFIER_MULTI_PART)
	# http_route_child_add (main_route, load_route)
	

def set_pipc_routes(http_cerver):

	http_cerver_static_path_add (http_cerver, b"./examples/http/public")

	# GET /api/pipc
	main_route = http_route_create (REQUEST_METHOD_GET, b"api/pipc", main_handler)
	http_cerver_route_register (http_cerver, main_route)

	set_organizaciones_routes (main_route) #OD
	set_usuarios_routes (main_route) #OD
	set_clientes_routes (main_route) #OD

	set_establecimientos_routes (main_route)
	set_tramites_routes (main_route)
	set_brigadas_routes (main_route)
	set_simulacros_routes (main_route)
	set_empleados_routes (main_route)
	set_programas_routes (main_route)

	
def start ():
	global web_service
	web_service = cerver_create_web (
		b"web-service", 8080, 10
	)

	# main configuration
	cerver_set_alias (web_service, b"web")

	cerver_set_receive_buffer_size (web_service, 4096)
	cerver_set_thpool_n_threads (web_service, 4)
	cerver_set_handler_type (web_service, CERVER_HANDLER_TYPE_THREADS)

	cerver_set_reusable_address_flags (web_service, True)

	# HTTP configuration
	http_cerver = http_cerver_get (web_service)

	# uploads
	http_cerver_set_uploads_path (http_cerver, b"/var/uploads")
	http_cerver_set_uploads_delete_when_done (http_cerver, True)
	http_cerver_set_default_uploads_filename_generator (http_cerver)

	set_pipc_routes(http_cerver)

	# start
	cerver_start (web_service)

if __name__ == "__main__":
	signal.signal (signal.SIGINT, end)
	signal.signal (signal.SIGTERM, end)
	signal.signal (signal.SIGPIPE, signal.SIG_IGN)

	cerver_init ()

	cerver_version_print_full ()

	pycerver_version_print_full ()

	if (db_mongo_init ()):
		start ()
