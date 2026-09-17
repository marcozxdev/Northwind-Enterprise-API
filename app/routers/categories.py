# app/routers/categories.py
#
# Endpoints para el recurso Categories (Categorias de productos).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/categories          -> Listar categorias
#   GET    /api/categories/{id}     -> Obtener una categoria
#   POST   /api/categories          -> Crear una categoria
#   PUT    /api/categories/{id}     -> Actualizar una categoria
#   DELETE /api/categories/{id}     -> Eliminar una categoria
#
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.categories import CategoryRepository
from app.schemas.categories import (
    CategoryCreate,
    CategoryList,
    CategoryResponse,
    CategoryUpdate,
)

router = APIRouter(prefix="/categories", tags=["Categorias"])


@router.get("/", response_model=CategoryList)
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista todas las categorias.

    GET /api/categories
    """
    repo = CategoryRepository(db)
    items, total = repo.get_all()
    return CategoryList(items=items, total=total)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene una categoria por ID.

    GET /api/categories/{category_id}
    """
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no encontrada",
        )

    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea una nueva categoria.

    POST /api/categories
    """
    repo = CategoryRepository(db)
    new_category = repo.create(data.model_dump())
    return new_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza una categoria.

    PUT /api/categories/{category_id}
    """
    repo = CategoryRepository(db)

    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no encontrada",
        )

    updated = repo.update(category_id, data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina una categoria.

    DELETE /api/categories/{category_id}
    """
    repo = CategoryRepository(db)

    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no encontrada",
        )

    repo.delete(category_id)
    return None
