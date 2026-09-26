# app/schemas/__init__.py
#
# Exportar todos los schemas para facilitar imports desde otros archivos.
#
# Uso:
#   from app.schemas import CustomerCreate, UserResponse, OrderList
#   from app.schemas.users import LoginRequest
#
from app.schemas.users import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    UserUpdate,
    UserUpdateRoles,
    UserList,
    RoleResponse,
    RoleList,
)
from app.schemas.customers import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerList,
)
from app.schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductList,
)
from app.schemas.orders import (
    OrderCreate,
    OrderDetailCreate,
    OrderUpdate,
    OrderResponse,
    OrderDetailResponse,
    OrderList,
)
from app.schemas.employees import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeTerritoryResponse,
    EmployeeList,
)
from app.schemas.categories import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryList,
)
from app.schemas.suppliers import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
    SupplierList,
)
from app.schemas.shippers import (
    ShipperCreate,
    ShipperUpdate,
    ShipperResponse,
    ShipperList,
)
from app.schemas.regions import (
    RegionCreate,
    RegionUpdate,
    RegionResponse,
    RegionList,
    TerritoryCreate,
    TerritoryUpdate,
    TerritoryResponse,
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
