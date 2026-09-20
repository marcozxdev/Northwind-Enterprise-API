# app/routers/__init__.py
#
# Exportar todos los routers para incluirlos en main.py.
#
from app.routers import auth, users, customers, products, orders, employees, categories, suppliers, shippers, regions

__all__ = [
    "auth",
    "users",
    "customers",
    "products",
    "orders",
    "employees",
    "categories",
    "suppliers",
    "shippers",
    "regions",
]
