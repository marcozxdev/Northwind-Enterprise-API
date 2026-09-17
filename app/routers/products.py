# app/routers/products.py
#
# Endpoints para el recurso Products (Productos).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/products          -> Listar productos (con filtros)
#   GET    /api/products/{id}     -> Obtener un producto
#   POST   /api/products          -> Crear un producto
#   PUT    /api/products/{id}     -> Actualizar un producto
#   DELETE /api/products/{id}     -> Eliminar un producto
#
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.products import ProductRepository
from app.schemas.products import (
    ProductCreate,
    ProductList,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("/", response_model=ProductList)
def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    discontinued: Optional[bool] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    in_stock: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista productos con filtros opcionales.

    GET /api/products?page=1&category_id=1&in_stock=true
    """
    repo = ProductRepository(db)
    items, total = repo.get_all_with_filters(
        page=page,
        per_page=per_page,
        category_id=category_id,
        supplier_id=supplier_id,
        discontinued=discontinued,
        price_min=price_min,
        price_max=price_max,
        in_stock=in_stock,
    )

    # Enriquecer con category_name y supplier_company
    enriched_items = []
    for product in items:
        item = ProductResponse.model_validate(product)
        if product.category:
            item.category_name = product.category.category_name
        if product.supplier:
            item.supplier_company = product.supplier.company_name
        enriched_items.append(item)

    return ProductList(items=enriched_items, total=total, page=page, per_page=per_page)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene un producto por ID.

    GET /api/products/{product_id}
    """
    repo = ProductRepository(db)
    product = repo.get_with_relations(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    response = ProductResponse.model_validate(product)
    if product.category:
        response.category_name = product.category.category_name
    if product.supplier:
        response.supplier_company = product.supplier.company_name

    return response


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea un nuevo producto.

    POST /api/products
    """
    repo = ProductRepository(db)
    new_product = repo.create(data.model_dump())
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza un producto.

    PUT /api/products/{product_id}
    """
    repo = ProductRepository(db)

    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    updated = repo.update(product_id, data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina un producto.

    DELETE /api/products/{product_id}
    """
    repo = ProductRepository(db)

    product = repo.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    repo.delete(product_id)
    return None
