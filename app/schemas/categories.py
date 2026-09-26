# app/schemas/categories.py
#
# Esquemas Pydantic para el recurso Categories (Categorias de productos).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   CategoryCreate:
#     - category_name: str [requerido, max 15]
#     - description:   str | None [opcional]
#
#   CategoryUpdate:
#     - Todos los campos opcionales.
#
#   CategoryResponse:
#     - category_id, category_name, description
#
#   CategoryList:
#     - items, total
#

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    """
    Cuerpo del request para POST /api/categories
    """
    category_name: str = Field(..., min_length=1, max_length=15)
    description: str | None = None


class CategoryUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/categories/{category_id}"""
    category_name: str | None = Field(None, max_length=15)
    description: str | None = None


class CategoryResponse(BaseModel):
    """
    Respuesta de una categoria.

    Config:
        - from_attributes = True
    """
    category_id: int
    category_name: str
    description: str | None

    model_config = {"from_attributes": True}


class CategoryList(BaseModel):
    """Lista de categorias (no paginada, son pocas)."""
    items: list[CategoryResponse]
    total: int
