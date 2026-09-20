# app/main.py
#
# Punto de entrada de la API Northwind Enterprise.
#
# Este archivo se encarga de:
#   1. Crear la instancia de FastAPI con metadatos (titulo, version, descripcion).
#   2. Incluir todos los routers (endpoints) desde la carpeta routers/.
#   3. Configurar middlewares (CORS).
#   4. Exponer la documentacion automatica en /docs y /redoc.
#
# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================
#
#   Autenticacion (publicos):
#     - POST /northwind/api/auth/register  -> Registrar nuevo usuario
#     - POST /northwind/api/auth/login     -> Iniciar sesion, obtener token JWT
#     - GET  /northwind/api/auth/me        -> Ver perfil del usuario autenticado
#
#   Usuarios (requieren auth + admin):
#     - GET    /northwind/api/users             -> Listar usuarios
#     - GET    /northwind/api/users/{id}        -> Ver usuario
#     - PUT    /northwind/api/users/{id}        -> Actualizar usuario
#     - DELETE /northwind/api/users/{id}        -> Desactivar usuario
#     - PUT    /northwind/api/users/{id}/roles  -> Asignar roles
#
#   Recursos Northwind (requieren auth + rol):
#     - /northwind/api/customers     -> CRUD de clientes
#     - /northwind/api/orders        -> CRUD de ordenes
#     - /northwind/api/products      -> CRUD de productos
#     - /northwind/api/employees     -> CRUD de empleados
#     - /northwind/api/categories    -> CRUD de categorias
#     - /northwind/api/suppliers     -> CRUD de proveedores
#     - /northwind/api/shippers      -> CRUD de transportistas
#     - /northwind/api/regions       -> CRUD de regiones
#     - /northwind/api/territories   -> CRUD de territorios
#
# ============================================================================
# FLUJO DE ARRANQUE
# ============================================================================
#
#   1. FastAPI crea la instancia "app".
#   2. Se incluyen los routers con prefijos /northwind/api/*.
#   3. Los requests pasan por: CORS -> Auth (si aplica) -> Endpoint -> Response.
#
# Ejecucion:
#   uvicorn app.main:app --reload --port 8000
#
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cache import close_redis, init_redis
from app.core.config import settings
from app.routers import (
    auth,
    categories,
    customers,
    employees,
    orders,
    products,
    regions,
    shippers,
    suppliers,
    users,
)

# Tags para documentacion Swagger
tags_metadata = [
    {"name": "Autenticacion", "description": "Login, registro y perfil"},
    {"name": "Usuarios", "description": "Gestion de usuarios (admin)"},
    {"name": "Clientes", "description": "CRUD de clientes"},
    {"name": "Productos", "description": "CRUD de productos"},
    {"name": "Ordenes", "description": "CRUD de ordenes de compra"},
    {"name": "Empleados", "description": "CRUD de empleados"},
    {"name": "Categorias", "description": "CRUD de categorias"},
    {"name": "Proveedores", "description": "CRUD de proveedores"},
    {"name": "Transportistas", "description": "CRUD de transportistas"},
    {"name": "Regiones", "description": "CRUD de regiones y territorios"},
]

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.app.NAME,
    version=settings.app.VERSION,
    description="API RESTful para la base de datos Northwind con autenticacion JWT",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Inicializar Redis al arrancar la app."""
    init_redis()


@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar Redis al apagar la app."""
    close_redis()


# Incluir routers
prefix = "/northwind/api"
app.include_router(auth.router, prefix=prefix)
app.include_router(users.router, prefix=prefix)
app.include_router(customers.router, prefix=prefix)
app.include_router(products.router, prefix=prefix)
app.include_router(orders.router, prefix=prefix)
app.include_router(employees.router, prefix=prefix)
app.include_router(categories.router, prefix=prefix)
app.include_router(suppliers.router, prefix=prefix)
app.include_router(shippers.router, prefix=prefix)
app.include_router(regions.router, prefix=prefix)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "app": settings.app.NAME,
        "version": settings.app.VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Verifica el estado de la API."""
    return {"status": "healthy"}
