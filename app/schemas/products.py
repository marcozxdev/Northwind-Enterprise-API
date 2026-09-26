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
    supplier_id: int | None = None
    category_id: int | None = None
    quantity_per_unit: str | None = Field(None, max_length=20)
    unit_price: float | None = Field(None, ge=0)
    units_in_stock: int | None = Field(None, ge=0)
    units_on_order: int | None = Field(None, ge=0)
    reorder_level: int | None = Field(None, ge=0)
    discontinued: int = Field(..., ge=0, le=1)


class ProductUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/products/{product_id}"""
    product_name: str | None = Field(None, max_length=40)
    supplier_id: int | None = None
    category_id: int | None = None
    quantity_per_unit: str | None = Field(None, max_length=20)
    unit_price: float | None = Field(None, ge=0)
    units_in_stock: int | None = Field(None, ge=0)
    units_on_order: int | None = Field(None, ge=0)
    reorder_level: int | None = Field(None, ge=0)
    discontinued: int | None = Field(None, ge=0, le=1)


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
    supplier_id: int | None
    category_id: int | None
    quantity_per_unit: str | None
    unit_price: float | None
    units_in_stock: int | None
    units_on_order: int | None
    reorder_level: int | None
    discontinued: int
    category_name: str | None = None
    supplier_company: str | None = None

    model_config = {"from_attributes": True}


class ProductList(BaseModel):
    """Respuesta paginada de productos."""
    items: list[ProductResponse]
    total: int
    page: int
    per_page: int
