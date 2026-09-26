# app/models/__init__.py
#
# Este archivo importa todos los modelos ORM para que SQLAlchemy los conozca.
#
# ============================================================================
# POR QUE EXISTE ESTE ARCHIVO?
# ============================================================================
#
# Cuando usas Base.metadata.create_all(), SQLAlchemy necesita saber todos
# los modelos que existen para crear las tablas. Si no los importas aqui,
# las tablas no se crean y las relaciones no funcionan.
#
# ============================================================================
# USO
# ============================================================================
#
#   # En database.py o main.py:
#   from app.models import Base
#   Base.metadata.create_all(bind=engine)
#
#   # Esto crea TODAS las tablas definidas en los modelos importados.
#
# ============================================================================
# ORDEN DE IMPORTACION
# ============================================================================
#
# El orden importa porque hay relaciones circulares (ej: Order -> Customer,
# Customer -> Order). SQLAlchemy maneja esto con "string references" (foreign_key
# como string en vez de clase), pero los imports deben estar en un orden que
# funcione.
#
# Orden recomendado:
#   1. Modelos sin dependencias: Region, Shipper, Supplier, Category, Role
#   2. Modelos con dependencias simples: Territory, Product, User
#   3. Modelos con dependencias complejas: Employee, Customer, Order
#   4. Tablas asociativas: EmployeeTerritory, UserRole
#

# Modelos de la base de datos Northwind
from app.models.categories import Category
from app.models.regions import Region, Territory, UsState
from app.models.shippers import Shipper
from app.models.suppliers import Supplier
from app.models.products import Product
from app.models.customers import Customer
from app.models.employees import Employee, EmployeeTerritory
from app.models.orders import Order, OrderDetail

# Modelos de autenticacion
from app.models.roles import Role
from app.models.users import User, user_roles


# Todos los modelos disponibles para importar desde otros archivos:
# from app.models import Customer, Order, Product, User, Role, ...
__all__ = [
    # Northwind
    "Category",
    "Region",
    "Territory",
    "UsState",
    "Shipper",
    "Supplier",
    "Product",
    "Customer",
    "Employee",
    "EmployeeTerritory",
    "Order",
    "OrderDetail",
    # Auth
    "Role",
    "User",
    "user_roles",
]
