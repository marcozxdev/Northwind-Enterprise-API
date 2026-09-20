# app/schemas/regions.py
#
# Esquemas Pydantic para el recurso Regions (Regiones y Territorios).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   RegionCreate:
#     - region_description: str [requerido]
#
#   RegionUpdate:
#     - region_description: str | None
#
#   RegionResponse:
#     - region_id, region_description
#
#   TerritoryCreate:
#     - territory_id:           str [requerido]
#     - territory_description:  str [requerido]
#     - region_id:              int [requerido]
#
#   TerritoryUpdate:
#     - Todos los campos opcionales.
#
#   TerritoryResponse:
#     - territory_id, territory_description, region_id, region_name
#
#   RegionList:
#     - items, total
#
from typing import Optional

from pydantic import BaseModel, Field


class RegionCreate(BaseModel):
    """
    Cuerpo del request para POST /api/regions
    """
    region_description: str = Field(..., min_length=1, max_length=60)


class RegionUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/regions/{region_id}"""
    region_description: Optional[str] = Field(None, max_length=60)


class RegionResponse(BaseModel):
    """
    Respuesta de una region.

    Config:
        - from_attributes = True
    """
    region_id: int
    region_description: str

    model_config = {"from_attributes": True}


class RegionList(BaseModel):
    """Lista de regiones (no paginada)."""
    items: list[RegionResponse]
    total: int


class TerritoryCreate(BaseModel):
    """
    Cuerpo del request para POST /api/territories
    """
    territory_id: str = Field(..., max_length=20)
    territory_description: str = Field(..., max_length=60)
    region_id: int


class TerritoryUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/territories/{territory_id}"""
    territory_description: Optional[str] = Field(None, max_length=60)
    region_id: Optional[int] = None


class TerritoryResponse(BaseModel):
    """
    Respuesta de un territorio.

    Config:
        - from_attributes = True
    """
    territory_id: str
    territory_description: str
    region_id: int
    region_name: Optional[str] = None

    model_config = {"from_attributes": True}
