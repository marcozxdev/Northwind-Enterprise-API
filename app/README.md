# app/

Directorio principal de la aplicacion FastAPI.

## Archivos

| Archivo | Descripcion |
|---|---|
| `main.py` | Punto de entrada de la API. Crea la instancia FastAPI, incluye routers, define middlewares y eventos. |
| `config.py` | Configuracion centralizada. Lee variables de entorno desde `.env` usando `pydantic-settings`. |
| `database.py` | Engine de SQLAlchemy, clase Base para modelos, sessionmaker y dependencia `get_db()`. |
| `dependencies.py` | Dependencias de autenticacion: `get_current_user`, `get_current_active_user`, `require_role`. |

## Subcarpetas

### `models/`
Modelos ORM SQLAlchemy que mapean las tablas de la BD Northwind.

```
models/
├── __init__.py      # Importa todos los modelos (necesario para create_all)
├── categories.py    # Category
├── regions.py       # Region, Territory, UsState
├── shippers.py      # Shipper
├── suppliers.py     # Supplier
├── products.py      # Product (FK: category, supplier)
├── customers.py     # Customer (relacion 1:N con orders)
├── employees.py     # Employee (self-ref via reports_to, M:N con territories)
├── orders.py        # Order, OrderDetail (FK: customer, employee, shipper)
├── roles.py         # Role (admin, user, viewer)
└── users.py         # User, user_roles (M:N con roles)
```

### `routers/`
Endpoints HTTP organizados por recurso.

### `schemas/`
Esquemas Pydantic para validacion y serializacion de datos.

## Diagrama de Relaciones

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  customers  │────<│    orders    │>────│  employees  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │                    │
                           │                    │
                    ┌──────────────┐     ┌──────────────┐
                    │ order_details│>────│   products   │
                    └──────────────┘     └──────────────┘
                                              │    │
                           ┌──────────────────┘    └──────────────────┐
                           │                                          │
                    ┌──────────────┐                          ┌──────────────┐
                    │  categories  │                          │  suppliers   │
                    └──────────────┘                          └──────────────┘

┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    users    │────<│  user_roles  │>────│    roles    │
└─────────────┘     └──────────────┘     └─────────────┘

┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   region    │────<│ territories  │>────│  employees  │
└─────────────┘     └──────────────┘     └─────────────┘
                          (via employee_territories)
```
