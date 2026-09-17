# app/routers/suppliers.py
#
# Endpoints para el recurso Suppliers (Proveedores).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/suppliers          -> Listar proveedores (con filtros)
#   GET    /api/suppliers/{id}     -> Obtener un proveedor
#   POST   /api/suppliers          -> Crear un proveedor
#   PUT    /api/suppliers/{id}     -> Actualizar un proveedor
#   DELETE /api/suppliers/{id}     -> Eliminar un proveedor
#
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.suppliers import SupplierRepository
from app.schemas.suppliers import (
    SupplierCreate,
    SupplierList,
    SupplierResponse,
    SupplierUpdate,
)

router = APIRouter(prefix="/suppliers", tags=["Proveedores"])


@router.get("/", response_model=SupplierList)
def list_suppliers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    country: Optional[str] = None,
    city: Optional[str] = None,
    company_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista proveedores con filtros opcionales.

    GET /api/suppliers?page=1&country=USA
    """
    repo = SupplierRepository(db)
    items, total = repo.get_all_with_filters(
        page=page,
        per_page=per_page,
        country=country,
        city=city,
        company_name=company_name,
    )
    return SupplierList(items=items, total=total, page=page, per_page=per_page)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene un proveedor por ID.

    GET /api/suppliers/{supplier_id}
    """
    repo = SupplierRepository(db)
    supplier = repo.get_by_id(supplier_id)

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )

    return supplier


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    data: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea un nuevo proveedor.

    POST /api/suppliers
    """
    repo = SupplierRepository(db)
    new_supplier = repo.create(data.model_dump())
    return new_supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza un proveedor.

    PUT /api/suppliers/{supplier_id}
    """
    repo = SupplierRepository(db)

    supplier = repo.get_by_id(supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )

    updated = repo.update(supplier_id, data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina un proveedor.

    DELETE /api/suppliers/{supplier_id}
    """
    repo = SupplierRepository(db)

    supplier = repo.get_by_id(supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )

    repo.delete(supplier_id)
    return None
