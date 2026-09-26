# app/schemas/__init__.py
#
# Exportar todos los schemas para facilitar imports desde otros archivos.
#
# Uso:
#   from app.schemas import CustomerCreate, UserResponse, OrderList
#   from app.schemas.users import LoginRequest
#
from app.schemas.categories import (
    CategoryCreate,
    CategoryList,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.customers import (
    CustomerCreate,
    CustomerList,
    CustomerResponse,
    CustomerUpdate,
)
from app.schemas.employees import (
    EmployeeCreate,
    EmployeeList,
    EmployeeResponse,
    EmployeeTerritoryResponse,
    EmployeeUpdate,
)
from app.schemas.orders import (
    OrderCreate,
    OrderDetailCreate,
    OrderDetailResponse,
    OrderList,
    OrderResponse,
    OrderUpdate,
)
from app.schemas.products import (
    ProductCreate,
    ProductList,
    ProductResponse,
    ProductUpdate,
)
from app.schemas.regions import (
    RegionCreate,
    RegionList,
    RegionResponse,
    RegionUpdate,
    TerritoryCreate,
    TerritoryResponse,
    TerritoryUpdate,
)
from app.schemas.shippers import (
    ShipperCreate,
    ShipperList,
    ShipperResponse,
    ShipperUpdate,
)
from app.schemas.suppliers import (
    SupplierCreate,
    SupplierList,
    SupplierResponse,
    SupplierUpdate,
)
from app.schemas.users import (
    LoginRequest,
    RegisterRequest,
    RoleList,
    RoleResponse,
    TokenResponse,
    UserList,
    UserResponse,
    UserUpdate,
    UserUpdateRoles,
)

__all__ = [
    # Users
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "UserResponse",
    "UserUpdate",
    "UserUpdateRoles",
    "UserList",
    "RoleResponse",
    "RoleList",
    # Customers
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "CustomerList",
    # Products
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductList",
    # Orders
    "OrderCreate",
    "OrderDetailCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderDetailResponse",
    "OrderList",
    # Employees
    "EmployeeCreate",
    "EmployeeUpdate",
    "EmployeeResponse",
    "EmployeeTerritoryResponse",
    "EmployeeList",
    # Categories
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    "CategoryList",
    # Suppliers
    "SupplierCreate",
    "SupplierUpdate",
    "SupplierResponse",
    "SupplierList",
    # Shippers
    "ShipperCreate",
    "ShipperUpdate",
    "ShipperResponse",
    "ShipperList",
    # Regions
    "RegionCreate",
    "RegionUpdate",
    "RegionResponse",
    "RegionList",
    "TerritoryCreate",
    "TerritoryUpdate",
    "TerritoryResponse",
]
