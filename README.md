# Northwind Enterprise API

API RESTful completa para la base de datos **Northwind** clásica de Microsoft.
Incluye autenticación JWT, roles, caché Redis, documentación automática y **100 tests**.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-8.1-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-100%20%E2%9C%93-brightgreen)

---

## Descripción

La **Northwind Enterprise API** es un **sistema backend empresarial completo** inspirado en [Northwind Traders](https://www.microsoft.com/en-us/power-platform/blog/power-apps/northwind-traders-relational-data-sample/), la famosa base de datos de Microsoft que simula una empresa ficticia de importación y exportación de alimentos especiales del mundo. Esta API replica ese escenario real usando tecnologías modernas: **PostgreSQL** como base de datos relacional, **FastAPI** como framework de alto rendimiento, y **Redis** para caché con baja latencia.

### Propósito educativo

El objetivo principal es **aprender a consumir una base de datos a través de una API REST**, **sin necesidad de escribir consultas SQL**. Toda la interacción con los datos se realiza mediante endpoints HTTP (GET, POST, PUT, DELETE), lo que permite entender cómo funciona un backend empresarial real sin necesitar conocimientos previos de SQL.

Inspirada en [pthom/northwind_psql](https://github.com/pthom/northwind_psql) (1k+ stars), que proporciona la base de datos Northwind para PostgreSQL con Docker, este proyecto toma esa base de datos y le agrega una capa de API REST completa para que puedas interactuar con los datos de una empresa de alimentos de forma realista.

### Lo que puedes aprender

- **Consumir datos sin SQL**: Consultar productos, clientes, órdenes, empleados, etc., solo con peticiones HTTP
- **Estudiar arquitectura backend**: Código limpio con patrón Repository, separación de capas, y schemas Pydantic para validación
- **Practicar autenticación JWT**: Sistema completo de registro, login y control de roles
- **Entender caché Redis**: Caché automática con TTLs e invalidación para baja latencia
- **Aprender testing**: 100 tests que validan cada funcionalidad
- **Usar Docker**: Levantar PostgreSQL, Redis, pgAdmin y la API con un solo comando

### Funcionalidades principales

- **Autenticación JWT** con registro, login y tokens de acceso
- **Sistema de roles** con 3 niveles: `admin`, `user`, `viewer`
- **CRUD completo** para 8 entidades: Products, Customers, Orders, Employees, Categories, Suppliers, Shippers, Regions
- **Caché Redis** con TTLs configurables e invalidación automática
- **Documentación automática** con Swagger UI y ReDoc
- **100 tests** unitarios y de integración con pytest
- **Docker** listo para producción con docker compose

---

## Sobre Northwind Traders

**Northwind Traders** es una empresa ficticia creada por Microsoft en 1992 como base de datos de ejemplo para Microsoft Access. Desde entonces, se ha convertido en el estándar de la industria para enseñar bases de datos relacionales, y ha inspirado proyectos como [Adventure Works](https://learn.microsoft.com/es-es/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms).

La empresa simula una compañía de **importación y exportación de alimentos especiales** del mundo, con:

- **Clientes**: Tiendas de comestibles independientes que compran productos
- **Productos**: Alimentos de categorías como Bebidas, Lácteos, Carnes, Frutas, etc.
- **Órdenes**: Pedidos con detalles (cantidades, precios, descuentos)
- **Empleados**: Vendedores que gestionan las ventas
- **Proveedores**: Empresas que suministran los productos
- **Transportistas**: Compañías de envío que entregan los pedidos
- **Regiones**: Territorios de venta en diferentes países

En esta API, puedes interactuar con todos estos datos como si fueras el backend de una empresa real de pedidos de alimentos.

---

## Stack tecnológico

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Framework | FastAPI | 0.141 |
| Lenguaje | Python | 3.12 |
| ORM | SQLAlchemy | 2.0 |
| Base de datos | PostgreSQL | 17 |
| Caché | Redis | 8.1 |
| Autenticación | JWT (python-jose) | - |
| Hash passwords | bcrypt | 5.0 |
| Schemas | Pydantic | 2.13 |
| Testing | pytest + httpx | 8.3 |
| Contenedores | Docker Compose | - |

---

## Quick Start con Docker (Recomendado)

La forma más rápida de ejecutar la API. Docker levanta todos los servicios automáticamente.

### 1. Clonar el repositorio

```bash
git clone https://github.com/marcozxdev/Northwind-Enterprise-API.git
cd Northwind-Enterprise-API
```

### 2. Levantar todos los servicios

```bash
docker compose up -d
```

### 3. Verificar que la API está corriendo

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{"status": "healthy"}
```

### 4. Abrir la documentación

```
Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
```

### Servicios levantados

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **API FastAPI** | `8000` | La API REST principal |
| **PostgreSQL** | `5432` | Base de datos relacional |
| **Redis** | `6379` | Servidor de caché |
| **pgAdmin** | `5050` | Interfaz web para gestionar PostgreSQL |

### Comandos útiles Docker

```bash
# Ver estado de los servicios
docker compose ps

# Ver logs de la API
docker compose logs -f api

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes (reset completo)
docker compose down -v

# Reiniciar solo la API
docker compose restart api
```

---

## Quick Start sin Docker (Local)

Si prefieres ejecutar la API directamente en tu máquina sin contenedores.

### 1. Requisitos previos

- Python 3.12 o superior
- PostgreSQL 17 corriendo localmente
- Redis corriendo localmente

### 2. Configurar el entorno

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar el archivo `.env` y cambiar las credenciales para apuntar a tu PostgreSQL y Redis locales:

```env
# Cambiar hosts a localhost
DB_HOST=localhost
REDIS_HOST=localhost

# Configurar tus credenciales de PostgreSQL
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=northwind
```

### 4. Crear la base de datos

```bash
# Conectar a PostgreSQL y crear la BD
psql -U tu_usuario -c "CREATE DATABASE northwind;"

# Ejecutar el script de inicialización
psql -U tu_usuario -d northwind -f database/init.sql
```

### 5. Ejecutar la API

```bash
uvicorn app.main:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`

### 6. Ejecutar los tests

```bash
pytest tests/ -v
```

---

## Documentación de la API (Swagger / ReDoc)

FastAPI genera documentación automáticamente a partir del código. No necesitas mantenimiento manual.

### URLs de documentación

| Herramienta | URL | Descripción |
|-------------|-----|-------------|
| **Swagger UI** | `http://localhost:8000/docs` | Interfaz interactiva para probar endpoints |
| **ReDoc** | `http://localhost:8000/redoc` | Documentación limpia y formal |
| **OpenAPI JSON** | `http://localhost:8000/openapi.json` | Esquema OpenAPI 3.1 completo |

### Cómo autenticarse desde Swagger UI

1. Abrir `http://localhost:8000/docs`
2. Expandir el endpoint `POST /northwind/api/auth/login`
3. Hacer clic en **"Try it out"**
4. Ingresar las credenciales:
   ```json
   {
     "username": "admin",
     "password": "Northwind2024!"
   }
   ```
5. Hacer clic en **"Execute"**
6. Copiar el valor de `access_token` de la respuesta
7. Hacer clic en el botón **"Authorize"** (parte superior de la página)
8. En el campo "Value", pegar: `Bearer tu_token_aqui`
9. Hacer clic en **"Authorize"** y luego **"Close"**
10. Ahora todos los endpoints autenticados están listos para usar

### Cómo probar un endpoint

1. Expandir cualquier endpoint (ej: `GET /northwind/api/products`)
2. Hacer clic en **"Try it out"**
3. Completar los parámetros si los hay
4. Hacer clic en **"Execute"**
5. Ver la respuesta con código de estado y body

---

## Endpoints disponibles

### Autenticación (públicos - no requieren token)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/northwind/api/auth/register` | Registrar nuevo usuario |
| `POST` | `/northwind/api/auth/login` | Iniciar sesión, obtener token JWT |
| `GET` | `/northwind/api/auth/me` | Ver perfil del usuario autenticado |

### Usuarios (requieren auth + rol admin)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/users` | Listar todos los usuarios |
| `GET` | `/northwind/api/users/{id}` | Ver un usuario por ID |
| `PUT` | `/northwind/api/users/{id}` | Actualizar datos de usuario |
| `DELETE` | `/northwind/api/users/{id}` | Desactivar usuario (soft delete) |
| `PUT` | `/northwind/api/users/{id}/roles` | Asignar roles a usuario |

### Productos (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/products` | Listar productos (con paginación y filtros) |
| `GET` | `/northwind/api/products/{id}` | Ver detalle de producto |
| `POST` | `/northwind/api/products` | Crear producto (admin, user) |
| `PUT` | `/northwind/api/products/{id}` | Actualizar producto (admin, user) |
| `DELETE` | `/northwind/api/products/{id}` | Eliminar producto (solo admin) |

**Filtros disponibles:** `?category_id=1`, `?min_price=10`, `?max_price=100`, `?in_stock=true`

### Clientes (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/customers` | Listar clientes (con paginación y filtros) |
| `GET` | `/northwind/api/customers/{id}` | Ver detalle de cliente |
| `POST` | `/northwind/api/customers` | Crear cliente (admin, user) |
| `PUT` | `/northwind/api/customers/{id}` | Actualizar cliente (admin, user) |
| `DELETE` | `/northwind/api/customers/{id}` | Eliminar cliente (solo admin) |

**Filtros disponibles:** `?country=Mexico`, `?city=Madrid`, `?company_name=Microsoft`

### Órdenes (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/orders` | Listar órdenes (con paginación y filtros) |
| `GET` | `/northwind/api/orders/{id}` | Ver orden con detalles (order_details) |
| `POST` | `/northwind/api/orders` | Crear orden con detalles (admin, user) |
| `PUT` | `/northwind/api/orders/{id}` | Actualizar orden (admin, user) |
| `DELETE` | `/northwind/api/orders/{id}` | Eliminar orden (solo admin) |

**Filtros disponibles:** `?customer_id=ALFKI`, `?employee_id=5`, `?shipped=true`

### Empleados (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/employees` | Listar empleados |
| `GET` | `/northwind/api/employees/{id}` | Ver empleado |
| `POST` | `/northwind/api/employees` | Crear empleado (admin, user) |
| `PUT` | `/northwind/api/employees/{id}` | Actualizar empleado (admin, user) |
| `DELETE` | `/northwind/api/employees/{id}` | Eliminar empleado (solo admin) |

### Categorías (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/categories` | Listar categorías |
| `GET` | `/northwind/api/categories/{id}` | Ver categoría |
| `POST` | `/northwind/api/categories` | Crear categoría (admin, user) |
| `PUT` | `/northwind/api/categories/{id}` | Actualizar categoría (admin, user) |
| `DELETE` | `/northwind/api/categories/{id}` | Eliminar categoría (solo admin) |

### Proveedores (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/suppliers` | Listar proveedores |
| `GET` | `/northwind/api/suppliers/{id}` | Ver proveedor |
| `POST` | `/northwind/api/suppliers` | Crear proveedor (admin, user) |
| `PUT` | `/northwind/api/suppliers/{id}` | Actualizar proveedor (admin, user) |
| `DELETE` | `/northwind/api/suppliers/{id}` | Eliminar proveedor (solo admin) |

### Transportistas (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/shippers` | Listar transportistas |
| `GET` | `/northwind/api/shippers/{id}` | Ver transportista |
| `POST` | `/northwind/api/shippers` | Crear transportista (admin, user) |
| `PUT` | `/northwind/api/shippers/{id}` | Actualizar transportista (admin, user) |
| `DELETE` | `/northwind/api/shippers/{id}` | Eliminar transportista (solo admin) |

### Regiones (requieren auth + rol)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/northwind/api/regions` | Listar regiones |
| `GET` | `/northwind/api/regions/{id}` | Ver región |
| `POST` | `/northwind/api/regions` | Crear región (admin, user) |
| `PUT` | `/northwind/api/regions/{id}` | Actualizar región (admin, user) |
| `DELETE` | `/northwind/api/regions/{id}` | Eliminar región (solo admin) |

### Health Check (públicos)

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Health check con info de la app |
| `GET` | `/health` | Verificación de estado |

---

## Variables de entorno

Todas las variables se configuran en el archivo `.env` en la raíz del proyecto.

```env
# =============================================================================
# APP
# =============================================================================
APP_NAME=Northwind Enterprise API
APP_VERSION=1.0.0
DEBUG=True

# =============================================================================
# BASE DE DATOS (PostgreSQL)
# =============================================================================
DB_USER=northwind_user
DB_PASSWORD=northwind_password
DB_NAME=northwind
DB_PORT=5432
DB_HOST=northwind_postgres    # Cambiar a "localhost" si ejecuta sin Docker

# =============================================================================
# JWT (Autenticación)
# =============================================================================
JWT_SECRET_KEY=YOUR-SECRET-key     # CAMBIAR en producción
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXP_MIN=40            # Expiración del token en minutos

# =============================================================================
# REDIS (Caché)
# =============================================================================
REDIS_PORT=6379
REDIS_HOST=northwind_redis         # Cambiar a "localhost" si ejecuta sin Docker

# =============================================================================
# PGADMIN (Interfaz de gestión de PostgreSQL)
# =============================================================================
PGADMIN_EMAIL=admin@northwind.com
PGADMIN_PASSWORD=admin123
```

### Variables importantes para producción

| Variable | Recomendación |
|----------|---------------|
| `JWT_SECRET_KEY` | Cambiar a una clave secreta fuerte y aleatoria |
| `DB_PASSWORD` | Usar una contraseña segura |
| `DEBUG` | Cambiar a `False` en producción |
| `allow_origins` en CORS | Restringir a dominios específicos en `app/main.py` |

---

## Testing

### Ejecutar todos los tests

```bash
# Con Docker
docker compose exec api pytest tests/ -v

# Sin Docker
pytest tests/ -v
```

### Ejecutar tests de un módulo específico

```bash
# Tests de autenticación
docker compose exec api pytest tests/test_auth.py -v

# Tests de productos
docker compose exec api pytest tests/test_products.py -v

# Tests de caché Redis
docker compose exec api pytest tests/test_cache.py -v
```

### Ejecutar un test específico

```bash
docker compose exec api pytest tests/test_products.py::TestCreateProduct::test_crear_producto -v
```

### Resumen de tests

| Archivo | Cantidad | Qué valida |
|---------|----------|-----------|
| `test_auth.py` | 13 | Login, registro, JWT, perfil, errores |
| `test_users.py` | 15 | CRUD, roles, desactivación, usuario inactivo |
| `test_customers.py` | 15 | CRUD, filtros (país, ciudad, empresa), permisos |
| `test_products.py` | 14 | CRUD, filtros (categoría, precio, stock), permisos |
| `test_orders.py` | 14 | CRUD con detalles, filtros, permisos |
| `test_cache.py` | 17 | Funciones Redis, cache hits, invalidación automática |
| **Total** | **100** | |

### Resultado esperado

```
======================= 100 passed, 11 warnings in 2.85s ========================
```

---

## Caché Redis

La API utiliza Redis para cachear respuestas frecuentes y reducir la carga en PostgreSQL.

### TTLs configurados por módulo

| Módulo | TTL (listas) | TTL (detalles) | Tipo de datos |
|--------|-------------|----------------|---------------|
| Products | 3 minutos | 5 minutos | Transaccionales |
| Customers | 3 minutos | 5 minutos | Transaccionales |
| Orders | 3 minutos | 5 minutos | Transaccionales |
| Employees | 3 minutos | 5 minutos | Transaccionales |
| Categories | 30 minutos | 30 minutos | Estáticos |
| Suppliers | 30 minutos | 30 minutos | Estáticos |
| Shippers | 30 minutos | 30 minutos | Estáticos |
| Regions | 30 minutos | 30 minutos | Estáticos |

### Cómo funciona la invalidación

- **POST** (Crear): Invalida el cache de listas del módulo
- **PUT** (Actualizar): Invalida el cache de listas y detalles del módulo
- **DELETE** (Eliminar): Invalida el cache de listas y detalles del módulo

Ejemplo: Si creas un producto nuevo (`POST /products`), se limpia automáticamente el cache de `products:list:*`, forzando que la próxima consulta `GET /products` obtenga datos frescos de PostgreSQL.

### Verificar que Redis funciona

```bash
# Conectar a Redis
docker compose exec northwind_redis redis-cli

# Ver keys cacheadas
KEYS *

# Ver valor de una key
GET "northwind:products:list"
```

---

## Usuarios de prueba

La base de datos viene precargada con 6 usuarios para testing.

| Usuario | Contraseña | ID | Rol(es) | Estado |
|---------|-----------|-----|---------|--------|
| `admin` | `Northwind2024!` | 1 | `admin` | Activo |
| `manager` | `Northwind2024!` | 2 | `admin`, `user` | Activo |
| `vendedor` | `Northwind2024!` | 3 | `user` | Activo |
| `viewer` | `Northwind2024!` | 4 | `viewer` | Activo |
| `auditor` | `Northwind2024!` | 5 | `user`, `viewer` | Activo |
| `inactive` | `Northwind2024!` | 6 | `user` | Inactivo |

### Permisos por rol

| Rol | Lectura | Escritura | Eliminar | Gestionar usuarios |
|-----|---------|-----------|----------|-------------------|
| `admin` | ✅ | ✅ | ✅ | ✅ |
| `user` | ✅ | ✅ | ❌ | ❌ |
| `viewer` | ✅ | ❌ | ❌ | ❌ |

---

## Estructura del proyecto

```
Northwind-Enterprise-API/
├── app/                          # Código fuente de la API
│   ├── core/                     # Configuración y utilidades centrales
│   │   ├── cache.py              # Redis client, decorator @cache_response
│   │   ├── config.py             # Settings con pydantic-settings
│   │   ├── database.py           # Engine, SessionLocal, Base, get_db
│   │   ├── dependencies.py       # Auth: get_current_user, require_role
│   │   └── security.py           # JWT: create/decode token, bcrypt hash
│   ├── models/                   # Modelos SQLAlchemy (ORM)
│   │   ├── product.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── employee.py
│   │   ├── category.py
│   │   ├── supplier.py
│   │   ├── shipper.py
│   │   ├── region.py
│   │   └── user.py
│   ├── repositories/             # Patrón Repository (CRUD genérico)
│   │   ├── base.py               # RepositoryBase[T] genérico
│   │   ├── products.py
│   │   ├── customers.py
│   │   ├── orders.py
│   │   ├── employees.py
│   │   ├── categories.py
│   │   ├── suppliers.py
│   │   ├── shippers.py
│   │   ├── regions.py
│   │   └── users.py
│   ├── routers/                  # Endpoints FastAPI
│   │   ├── auth.py               # Login, register, me
│   │   ├── users.py              # CRUD usuarios + roles
│   │   ├── products.py           # CRUD productos + cache
│   │   ├── customers.py          # CRUD clientes + cache
│   │   ├── orders.py             # CRUD órdenes + cache
│   │   ├── employees.py          # CRUD empleados + cache
│   │   ├── categories.py         # CRUD categorías + cache
│   │   ├── suppliers.py          # CRUD proveedores + cache
│   │   ├── shippers.py           # CRUD transportistas + cache
│   │   └── regions.py            # CRUD regiones + cache
│   ├── schemas/                  # Schemas Pydantic (validación)
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── customers.py
│   │   ├── orders.py
│   │   ├── employees.py
│   │   ├── categories.py
│   │   ├── suppliers.py
│   │   ├── shippers.py
│   │   ├── regions.py
│   │   └── __init__.py
│   └── main.py                   # Punto de entrada de la app
├── database/
│   ├── init.sql                  # Script de inicialización de BD
│   └── seed.py                   # Script de seed (roles + admin)
├── tests/                        # 100 tests con pytest
│   ├── conftest.py               # Fixtures: client, auth headers, db
│   ├── test_auth.py              # Tests de autenticación
│   ├── test_users.py             # Tests de usuarios
│   ├── test_customers.py         # Tests de clientes
│   ├── test_products.py          # Tests de productos
│   ├── test_orders.py            # Tests de órdenes
│   └── test_cache.py             # Tests de caché Redis
├── docker-compose.yml            # Orquestación de servicios
├── Dockerfile                    # Imagen de la API
├── requirements.txt              # Dependencias Python
├── .env                          # Variables de entorno
├── .env.example                  # Plantilla de variables
├── .gitignore                    # Archivos ignorados por Git
└── README.md                     # Este archivo
```

---

## pgAdmin (Gestión de PostgreSQL)

pgAdmin es una interfaz web para gestionar la base de datos PostgreSQL visualmente.

### Acceder a pgAdmin

```
URL:      http://localhost:5050
Email:    admin@northwind.com
Password: admin123
```

### Conectar a la base de datos

1. Abrir pgAdmin en el navegador
2. Hacer clic en **"Add New Server"**
3. Pestaña **General**:
   - Name: `Northwind`
4. Pestaña **Connection**:
   - Host name/address: `northwind_postgres` (o `localhost` si es local)
   - Port: `5432`
   - Maintenance database: `northwind`
   - Username: `northwind_user`
   - Password: `northwind_password`
5. Hacer clic en **"Save"**

Ahora puedes explorar tablas, ejecutar queries, ver datos, etc.

---

## Health Check

La API expone dos endpoints para verificar su estado:

```bash
# Info general
curl http://localhost:8000/
```

```json
{
  "app": "Northwind Enterprise API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs"
}
```

```bash
# Health check
curl http://localhost:8000/health
```

```json
{
  "status": "healthy"
}
```
