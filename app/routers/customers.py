# app/routers/customers.py
#
# Endpoints para el recurso Customers (Clientes).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/customers          -> Listar clientes (con filtros)
#   GET    /api/customers/{id}     -> Obtener un cliente
#   POST   /api/customers          -> Crear un cliente
#   PUT    /api/customers/{id}     -> Actualizar un cliente
#   DELETE /api/customers/{id}     -> Eliminar un cliente
#
# ============================================================================
# CACHE
# ============================================================================
#
#   GET endpoints usan Redis cache con TTL de 3 min (list) y 5 min (detail).
#   POST/PUT/DELETE invalidan el cache de customers.
#

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.cache import cache_response, delete_cache_pattern
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.customers import CustomerRepository
from app.schemas.customers import (
    CustomerCreate,
    CustomerList,
    CustomerResponse,
    CustomerUpdate,
)

router = APIRouter(prefix="/customers", tags=["Clientes"])


@router.get("/", response_model=CustomerList)
@cache_response(ttl=180, prefix="customers:list")
def list_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    company_name: str | None = None,
    city: str | None = None,
    country: str | None = None,
    contact_title: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista clientes con filtros opcionales.

    GET /api/customers?page=1&company_name=alice&country=USA

    Cache: 180 segundos (3 min)
    """
    repo = CustomerRepository(db)
    items, total = repo.get_all_with_filters(
        page=page,
        per_page=per_page,
        company_name=company_name,
        city=city,
        country=country,
        contact_title=contact_title,
    )
    return CustomerList(items=items, total=total, page=page, per_page=per_page)


@router.get("/{customer_id}", response_model=CustomerResponse)
@cache_response(ttl=300, prefix="customers:get")
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene un cliente por ID.

    GET /api/customers/{customer_id}

    Cache: 300 segundos (5 min)
    """
    repo = CustomerRepository(db)
    customer = repo.get_by_id(customer_id)

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    return customer


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea un nuevo cliente.

    POST /api/customers

    Invalida cache de customers.
    """
    repo = CustomerRepository(db)

    existing = repo.get_by_id(data.customer_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con ese ID",
        )

    new_customer = repo.create(data.model_dump())

    # Invalidar cache
    delete_cache_pattern("customers:*")

    return new_customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: str,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza un cliente.

    PUT /api/customers/{customer_id}

    Invalida cache de customers.
    """
    repo = CustomerRepository(db)

    customer = repo.get_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    updated = repo.update(customer_id, data.model_dump(exclude_unset=True))

    # Invalidar cache
    delete_cache_pattern("customers:*")

    return updated


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina un cliente.

    DELETE /api/customers/{customer_id}

    Invalida cache de customers.
    """
    repo = CustomerRepository(db)

    customer = repo.get_by_id(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    repo.delete(customer_id)

    # Invalidar cache
    delete_cache_pattern("customers:*")

    return None
