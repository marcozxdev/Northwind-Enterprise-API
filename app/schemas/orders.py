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
from typing import Optional

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
    customer_id: Optional[str] = None
    employee_id: Optional[int] = None
    order_date: Optional[date] = None
    required_date: Optional[date] = None
    shipped_date: Optional[date] = None
    ship_via: Optional[int] = None
    freight: Optional[float] = None
    ship_name: Optional[str] = Field(None, max_length=40)
    ship_address: Optional[str] = Field(None, max_length=60)
    ship_city: Optional[str] = Field(None, max_length=15)
    ship_region: Optional[str] = Field(None, max_length=15)
    ship_postal_code: Optional[str] = Field(None, max_length=10)
    ship_country: Optional[str] = Field(None, max_length=15)
    details: list[OrderDetailCreate] = []


class OrderUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/orders/{order_id}"""
    customer_id: Optional[str] = None
    employee_id: Optional[int] = None
    order_date: Optional[date] = None
    required_date: Optional[date] = None
    shipped_date: Optional[date] = None
    ship_via: Optional[int] = None
    freight: Optional[float] = None
    ship_name: Optional[str] = Field(None, max_length=40)
    ship_address: Optional[str] = Field(None, max_length=60)
    ship_city: Optional[str] = Field(None, max_length=15)
    ship_region: Optional[str] = Field(None, max_length=15)
    ship_postal_code: Optional[str] = Field(None, max_length=10)
    ship_country: Optional[str] = Field(None, max_length=15)


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
    subtotal: Optional[float] = None
    product_name: Optional[str] = None

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
    customer_id: Optional[str]
    employee_id: Optional[int]
    order_date: Optional[date]
    required_date: Optional[date]
    shipped_date: Optional[date]
    ship_via: Optional[int]
    freight: Optional[float]
    ship_name: Optional[str]
    ship_address: Optional[str]
    ship_city: Optional[str]
    ship_region: Optional[str]
    ship_postal_code: Optional[str]
    ship_country: Optional[str]
    details: list[OrderDetailResponse] = []
    customer_name: Optional[str] = None
    employee_name: Optional[str] = None
    shipper_name: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderList(BaseModel):
    """Respuesta paginada de ordenes."""
    items: list[OrderResponse]
    total: int
    page: int
    per_page: int
