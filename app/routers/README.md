# routers/

Endpoints de la API REST. Cada archivo define las rutas HTTP para un recurso de la base de datos Northwind.

## Estructura

Cada router es un `APIRouter` de FastAPI que se incluye en `main.py`.

## Archivos

| Archivo | Recurso | Descripcion |
|---|---|---|
| `customers.py` | `/api/customers` | CRUD de clientes (GET, POST, PUT, DELETE) |
| `orders.py` | `/api/orders` | CRUD de ordenes con filtros por fecha, cliente, empleado |
| `products.py` | `/api/products` | CRUD de productos con filtros por categoria, proveedor |
| `employees.py` | `/api/employees` | CRUD de empleados |
| `categories.py` | `/api/categories` | CRUD de categorias de productos |
| `suppliers.py` | `/api/suppliers` | CRUD de proveedores |
| `shippers.py` | `/api/shippers` | CRUD de transportistas |
| `regions.py` | `/api/regions` | CRUD de regiones y territorios |
