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
from typing import Optional

from pydantic import BaseModel, Field


class SupplierCreate(BaseModel):
    """
    Cuerpo del request para POST /api/suppliers
    """
    company_name: str = Field(..., min_length=1, max_length=40)
    contact_name: Optional[str] = Field(None, max_length=30)
    contact_title: Optional[str] = Field(None, max_length=30)
    address: Optional[str] = Field(None, max_length=60)
    city: Optional[str] = Field(None, max_length=15)
    region: Optional[str] = Field(None, max_length=15)
    postal_code: Optional[str] = Field(None, max_length=10)
    country: Optional[str] = Field(None, max_length=15)
    phone: Optional[str] = Field(None, max_length=24)
    fax: Optional[str] = Field(None, max_length=24)
    homepage: Optional[str] = None


class SupplierUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/suppliers/{supplier_id}"""
    company_name: Optional[str] = Field(None, max_length=40)
    contact_name: Optional[str] = Field(None, max_length=30)
    contact_title: Optional[str] = Field(None, max_length=30)
    address: Optional[str] = Field(None, max_length=60)
    city: Optional[str] = Field(None, max_length=15)
    region: Optional[str] = Field(None, max_length=15)
    postal_code: Optional[str] = Field(None, max_length=10)
    country: Optional[str] = Field(None, max_length=15)
    phone: Optional[str] = Field(None, max_length=24)
    fax: Optional[str] = Field(None, max_length=24)
    homepage: Optional[str] = None


class SupplierResponse(BaseModel):
    """
    Respuesta de un proveedor.

    Config:
        - from_attributes = True
    """
    supplier_id: int
    company_name: str
    contact_name: Optional[str]
    contact_title: Optional[str]
    address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    fax: Optional[str]
    homepage: Optional[str]

    model_config = {"from_attributes": True}


class SupplierList(BaseModel):
    """Respuesta paginada de proveedores."""
    items: list[SupplierResponse]
    total: int
    page: int
    per_page: int
