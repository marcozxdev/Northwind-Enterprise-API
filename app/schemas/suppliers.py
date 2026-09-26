# app/schemas/suppliers.py
#
# Esquemas Pydantic para el recurso Suppliers (Proveedores).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   SupplierCreate:
#     - company_name:  str [requerido]
#     - contact_name:  str | None
#     - contact_title: str | None
#     - address:       str | None
#     - city:          str | None
#     - region:        str | None
#     - postal_code:   str | None
#     - country:       str | None
#     - phone:         str | None
#     - fax:           str | None
#     - homepage:      str | None
#
#   SupplierUpdate:
#     - Todos los campos opcionales.
#
#   SupplierResponse:
#     - Todos los campos de la tabla suppliers.
#
#   SupplierList:
#     - items, total, page, per_page
#

from pydantic import BaseModel, Field


class SupplierCreate(BaseModel):
    """
    Cuerpo del request para POST /api/suppliers
    """
    company_name: str = Field(..., min_length=1, max_length=40)
    contact_name: str | None = Field(None, max_length=30)
    contact_title: str | None = Field(None, max_length=30)
    address: str | None = Field(None, max_length=60)
    city: str | None = Field(None, max_length=15)
    region: str | None = Field(None, max_length=15)
    postal_code: str | None = Field(None, max_length=10)
    country: str | None = Field(None, max_length=15)
    phone: str | None = Field(None, max_length=24)
    fax: str | None = Field(None, max_length=24)
    homepage: str | None = None


class SupplierUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/suppliers/{supplier_id}"""
    company_name: str | None = Field(None, max_length=40)
    contact_name: str | None = Field(None, max_length=30)
    contact_title: str | None = Field(None, max_length=30)
    address: str | None = Field(None, max_length=60)
    city: str | None = Field(None, max_length=15)
    region: str | None = Field(None, max_length=15)
    postal_code: str | None = Field(None, max_length=10)
    country: str | None = Field(None, max_length=15)
    phone: str | None = Field(None, max_length=24)
    fax: str | None = Field(None, max_length=24)
    homepage: str | None = None


class SupplierResponse(BaseModel):
    """
    Respuesta de un proveedor.

    Config:
        - from_attributes = True
    """
    supplier_id: int
    company_name: str
    contact_name: str | None
    contact_title: str | None
    address: str | None
    city: str | None
    region: str | None
    postal_code: str | None
    country: str | None
    phone: str | None
    fax: str | None
    homepage: str | None

    model_config = {"from_attributes": True}


class SupplierList(BaseModel):
    """Respuesta paginada de proveedores."""
    items: list[SupplierResponse]
    total: int
    page: int
    per_page: int
