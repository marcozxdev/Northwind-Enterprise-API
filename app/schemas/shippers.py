# app/schemas/shippers.py
#
# Esquemas Pydantic para el recurso Shippers (Transportistas).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   ShipperCreate:
#     - company_name: str [requerido]
#     - phone:        str | None
#
#   ShipperUpdate:
#     - Todos los campos opcionales.
#
#   ShipperResponse:
#     - shipper_id, company_name, phone
#
#   ShipperList:
#     - items, total
#
from typing import Optional

from pydantic import BaseModel, Field


class ShipperCreate(BaseModel):
    """
    Cuerpo del request para POST /api/shippers
    """
    company_name: str = Field(..., min_length=1, max_length=40)
    phone: Optional[str] = Field(None, max_length=24)


class ShipperUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/shippers/{shipper_id}"""
    company_name: Optional[str] = Field(None, max_length=40)
    phone: Optional[str] = Field(None, max_length=24)


class ShipperResponse(BaseModel):
    """
    Respuesta de un transportista.

    Config:
        - from_attributes = True
    """
    shipper_id: int
    company_name: str
    phone: Optional[str]

    model_config = {"from_attributes": True}


class ShipperList(BaseModel):
    """Lista de transportistas (no paginada, son 3)."""
    items: list[ShipperResponse]
    total: int
