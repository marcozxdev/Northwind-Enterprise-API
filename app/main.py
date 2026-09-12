# app/main.py
#
# Punto de entrada de la API Northwind Enterprise.
#
# Este archivo se encarga de:
#   1. Crear la instancia de FastAPI con metadatos (titulo, version, descripcion).
#   2. Incluir todos los routers (endpoints) desde la carpeta routers/.
#   3. Definir eventos de startup y shutdown (conexion a BD, cache, etc.).
#   4. Configurar middlewares (CORS, logging, manejo de errores globales).
#   5. Exponer la documentacion automatica en /docs y /redoc.
#
# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================
#
#   Autenticacion (publicos):
#     - POST /api/auth/register  -> Registrar nuevo usuario
#     - POST /api/auth/login     -> Iniciar sesion, obtener token JWT
#     - GET  /api/auth/me        -> Ver perfil del usuario autenticado
#
#   Usuarios (requieren auth):
#     - GET    /api/users             -> Listar usuarios (admin)
#     - GET    /api/users/{id}        -> Ver usuario (admin o self)
#     - PUT    /api/users/{id}        -> Actualizar usuario (admin o self)
#     - DELETE /api/users/{id}        -> Desactivar usuario (admin)
#     - PUT    /api/users/{id}/roles  -> Asignar roles (admin)
#
#   Recursos Northwind (requieren auth + rol):
#     - /api/customers     -> CRUD de clientes
#     - /api/orders        -> CRUD de ordenes
#     - /api/products      -> CRUD de productos
#     - /api/employees     -> CRUD de empleados
#     - /api/categories    -> CRUD de categorias
#     - /api/suppliers     -> CRUD de proveedores
#     - /api/shippers      -> CRUD de transportistas
#     - /api/regions       -> CRUD de regiones
#
# ============================================================================
# FLUJO DE ARRANQUE
# ============================================================================
#
#   1. FastAPI crea la instancia "app".
#   2. Se incluyen los routers con prefijos /api/*.
#   3. Al recibir el primer request, se conecta a la BD.
#   4. Los requests pasan por: CORS -> Auth (si aplica) -> Endpoint -> Response.
#
# Ejecucion:
#   uvicorn app.main:app --reload --port 8000
#   (o desde Docker: docker-compose up api)
#





from fastapi import APIRouter, FastAPI

prefix = "northwind/api"
app  = FastAPI()


