# app/schemas/products.py
#
# Esquemas Pydantic para el recurso Products (Productos).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   ProductCreate (request body para POST):
#     - product_name:       str              [requerido]
#     - supplier_id:        int | None       [opcional, proveedor]
#     - category_id:        int | None       [opcional, categoria]
#     - quantity_per_unit:  str | None       [opcional]
#     - unit_price:         float | None     [opcional, precio]
#     - units_in_stock:     int | None       [opcional]
#     - units_on_order:     int | None       [opcional]
#     - reorder_level:      int | None       [opcional]
#     - discontinued:       int              [requerido, 0=activo, 1=inactivo]
#
#   ProductUpdate (request body para PUT/PATCH):
#     - Todos los campos de ProductCreate pero opcionales.
#
#   ProductResponse (response body):
#     - Todos los campos de la tabla products.
#     - Incluye category_name y supplier_company (join).
#     - Config: from_attributes = True
#
#   ProductList (respuesta paginada):
#     - items:    list[ProductResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """
    Cuerpo del request para POST /api/products

    Campos:
        - product_name:      str [requerido, max 40]
        - supplier_id:       int | None [opcional]
        - category_id:       int | None [opcional]
        - quantity_per_unit: str | None [opcional]
        - unit_price:        float | None [opcional, >= 0]
        - units_in_stock:    int | None [opcional, >= 0]
        - units_on_order:    int | None [opcional, >= 0]
        - reorder_level:     int | None [opcional, >= 0]
        - discontinued:      int [requerido, 0 o 1]
    """
    product_name: str = Field(..., min_length=1, max_length=40)
    supplier_id: Optional[int] = None
    category_id: Optional[int] = None
    quantity_per_unit: Optional[str] = Field(None, max_length=20)
    unit_price: Optional[float] = Field(None, ge=0)
    units_in_stock: Optional[int] = Field(None, ge=0)
    units_on_order: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    discontinued: int = Field(..., ge=0, le=1)


class ProductUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/products/{product_id}"""
    product_name: Optional[str] = Field(None, max_length=40)
    supplier_id: Optional[int] = None
    category_id: Optional[int] = None
    quantity_per_unit: Optional[str] = Field(None, max_length=20)
    unit_price: Optional[float] = Field(None, ge=0)
    units_in_stock: Optional[int] = Field(None, ge=0)
    units_on_order: Optional[int] = Field(None, ge=0)
    reorder_level: Optional[int] = Field(None, ge=0)
    discontinued: Optional[int] = Field(None, ge=0, le=1)


class ProductResponse(BaseModel):
    """
    Respuesta de un producto.

    Incluye:
        - Todos los campos de la tabla products
        - category_name: str | None (nombre de la categoria)
        - supplier_company: str | None (nombre del proveedor)
    """
    product_id: int
    product_name: str
    supplier_id: Optional[int]
    category_id: Optional[int]
    quantity_per_unit: Optional[str]
    unit_price: Optional[float]
    units_in_stock: Optional[int]
    units_on_order: Optional[int]
    reorder_level: Optional[int]
    discontinued: int
    category_name: Optional[str] = None
    supplier_company: Optional[str] = None

    model_config = {"from_attributes": True}


class ProductList(BaseModel):
    """Respuesta paginada de productos."""
    items: list[ProductResponse]
    total: int
    page: int
    per_page: int
