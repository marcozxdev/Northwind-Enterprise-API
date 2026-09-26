# app/schemas/orders.py
#
# Esquemas Pydantic para el recurso Orders (Ordenes de compra).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   OrderCreate (request body para POST):
#     - customer_id:      str | None
#     - employee_id:      int | None
#     - order_date:       date | None
#     - required_date:    date | None
#     - shipped_date:     date | None
#     - ship_via:         int | None
#     - freight:          float | None
#     - ship_name:        str | None
#     - ship_address:     str | None
#     - ship_city:        str | None
#     - ship_region:      str | None
#     - ship_postal_code: str | None
#     - ship_country:     str | None
#     - details:          list[OrderDetailCreate]
#
#   OrderDetailCreate:
#     - product_id:  int
#     - unit_price:  float
#     - quantity:    int
#     - discount:    float
#
#   OrderResponse (response body):
#     - Todos los campos de la tabla orders.
#     - details: list[OrderDetailResponse]
#     - customer_name, employee_name, shipper_name (joins)
#
#   OrderList (respuesta paginada):
#     - items, total, page, per_page
#
from datetime import date

from pydantic import BaseModel, Field


class OrderDetailCreate(BaseModel):
    """
    Detalle de una linea de orden (order_details).

    Campos:
        - product_id: int [requerido]
        - unit_price: float [requerido, >= 0]
        - quantity:   int [requerido, >= 1]
        - discount:   float [requerido, 0-1]
    """
    product_id: int
    unit_price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=1)
    discount: float = Field(0, ge=0, le=1)


class OrderCreate(BaseModel):
    """
    Cuerpo del request para POST /api/orders
    """
    customer_id: str | None = None
    employee_id: int | None = None
    order_date: date | None = None
    required_date: date | None = None
    shipped_date: date | None = None
    ship_via: int | None = None
    freight: float | None = None
    ship_name: str | None = Field(None, max_length=40)
    ship_address: str | None = Field(None, max_length=60)
    ship_city: str | None = Field(None, max_length=15)
    ship_region: str | None = Field(None, max_length=15)
    ship_postal_code: str | None = Field(None, max_length=10)
    ship_country: str | None = Field(None, max_length=15)
    details: list[OrderDetailCreate] = []


class OrderUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/orders/{order_id}"""
    customer_id: str | None = None
    employee_id: int | None = None
    order_date: date | None = None
    required_date: date | None = None
    shipped_date: date | None = None
    ship_via: int | None = None
    freight: float | None = None
    ship_name: str | None = Field(None, max_length=40)
    ship_address: str | None = Field(None, max_length=60)
    ship_city: str | None = Field(None, max_length=15)
    ship_region: str | None = Field(None, max_length=15)
    ship_postal_code: str | None = Field(None, max_length=10)
    ship_country: str | None = Field(None, max_length=15)


class OrderDetailResponse(BaseModel):
    """
    Respuesta de un detalle de orden.

    Incluye:
        - order_id, product_id, unit_price, quantity, discount
        - subtotal: unit_price * quantity * (1 - discount)
        - product_name: str | None (join)
    """
    order_id: int
    product_id: int
    unit_price: float
    quantity: int
    discount: float
    subtotal: float | None = None
    product_name: str | None = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    """
    Respuesta de una orden completa.

    Incluye:
        - Todos los campos de la tabla orders
        - details: list[OrderDetailResponse]
        - customer_name, employee_name, shipper_name (joins)
    """
    order_id: int
    customer_id: str | None
    employee_id: int | None
    order_date: date | None
    required_date: date | None
    shipped_date: date | None
    ship_via: int | None
    freight: float | None
    ship_name: str | None
    ship_address: str | None
    ship_city: str | None
    ship_region: str | None
    ship_postal_code: str | None
    ship_country: str | None
    details: list[OrderDetailResponse] = []
    customer_name: str | None = None
    employee_name: str | None = None
    shipper_name: str | None = None

    model_config = {"from_attributes": True}


class OrderList(BaseModel):
    """Respuesta paginada de ordenes."""
    items: list[OrderResponse]
    total: int
    page: int
    per_page: int
