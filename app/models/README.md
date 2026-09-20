# models/

Modelos SQLAlchemy ORM que mapean las tablas de la base de datos Northwind a objetos Python.

## Convenciones

- Cada archivo corresponde a una tabla de la BD.
- Se usa `DeclarativeBase` de SQLAlchemy 2.0.
- Las relaciones entre tablas se definen con `relationship()`.
- Los campos `NOT NULL` se definen como `nullable=False`.

## Archivos

| Archivo | Tabla |
|---|---|
| `customers.py` | `customers` |
| `orders.py` | `orders`, `order_details` |
| `products.py` | `products` |
| `employees.py` | `employees`, `employee_territories` |
| `categories.py` | `categories` |
| `suppliers.py` | `suppliers` |
| `shippers.py` | `shippers` |
| `regions.py` | `region`, `territories`, `us_states` |
