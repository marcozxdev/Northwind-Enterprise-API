# app/routers/__init__.py
#
# Exportar todos los routers para incluirlos en main.py.
#
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
