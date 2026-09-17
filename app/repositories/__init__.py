# app/repositories/__init__.py
#
# Exportar todos los repositories para facilitar imports.
#
# Uso:
#   from app.repositories import CustomerRepository, UserRepository
#   from app.repositories.users import UserRepository
#
from app.repositories.base import BaseRepository
from app.repositories.users import UserRepository
from app.repositories.customers import CustomerRepository
from app.repositories.products import ProductRepository
from app.repositories.orders import OrderRepository
from app.repositories.employees import EmployeeRepository
from app.repositories.categories import CategoryRepository
from app.repositories.suppliers import SupplierRepository
from app.repositories.shippers import ShipperRepository
from app.repositories.regions import RegionRepository, TerritoryRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "CustomerRepository",
    "ProductRepository",
    "OrderRepository",
    "EmployeeRepository",
    "CategoryRepository",
    "SupplierRepository",
    "ShipperRepository",
    "RegionRepository",
    "TerritoryRepository",
]
