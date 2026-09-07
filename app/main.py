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
# Endpoints esperados:
#   - /api/customers     -> CRUD de clientes
#   - /api/orders        -> CRUD de ordenes
#   - /api/products      -> CRUD de productos
#   - /api/employees     -> CRUD de empleados
#   - /api/categories    -> CRUD de categorias
#   - /api/suppliers     -> CRUD de proveedores
#   - /api/shippers      -> CRUD de transportistas
#   - /api/regions       -> CRUD de regiones
#   - /api/auth          -> Autenticacion (login, registro, refresh token)
#
# Ejecucion:
#   uvicorn app.main:app --reload --port 8000
#
