# app/routers/orders.py
#
# Endpoints para el recurso Orders (Ordenes de compra).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/orders                -> Listar ordenes (con filtros)
#   GET    /api/orders/{id}           -> Obtener una orden con detalles
#   POST   /api/orders                -> Crear una orden (con detalles)
#   PUT    /api/orders/{id}           -> Actualizar una orden
#   DELETE /api/orders/{id}           -> Eliminar una orden
#
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.orders import OrderRepository
from app.schemas.orders import (
    OrderCreate,
    OrderDetailResponse,
    OrderList,
    OrderResponse,
    OrderUpdate,
)

router = APIRouter(prefix="/orders", tags=["Ordenes"])


def _enrich_order(order) -> OrderResponse:
    """Enriquece una orden con nombres de relaciones."""
    response = OrderResponse.model_validate(order)
    if order.customer:
        response.customer_name = order.customer.company_name
    if order.employee:
        response.employee_name = f"{order.employee.first_name} {order.employee.last_name}"
    if order.shipper:
        response.shipper_name = order.shipper.company_name
    if order.details:
        enriched_details = []
        for detail in order.details:
            detail_resp = OrderDetailResponse.model_validate(detail)
            detail_resp.subtotal = detail.subtotal
            if detail.product:
                detail_resp.product_name = detail.product.product_name
            enriched_details.append(detail_resp)
        response.details = enriched_details
    return response


@router.get("/", response_model=OrderList)
def list_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    customer_id: Optional[str] = None,
    employee_id: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    shipped: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista ordenes con filtros opcionales.

    GET /api/orders?page=1&customer_id=ALFKI&shipped=false
    """
    repo = OrderRepository(db)
    items, total = repo.get_all_with_filters(
        page=page,
        per_page=per_page,
        customer_id=customer_id,
        employee_id=employee_id,
        date_from=date_from,
        date_to=date_to,
        shipped=shipped,
    )

    enriched_items = [_enrich_order(order) for order in items]
    return OrderList(items=enriched_items, total=total, page=page, per_page=per_page)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene una orden con todos sus detalles.

    GET /api/orders/{order_id}
    """
    repo = OrderRepository(db)
    order = repo.get_with_details(order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    return _enrich_order(order)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea una orden con sus detalles.

    POST /api/orders
    """
    repo = OrderRepository(db)

    order_data = data.model_dump(exclude={"details"})
    details_data = [d.model_dump() for d in data.details]

    new_order = repo.create_with_details(order_data, details_data)
    return _enrich_order(new_order)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza una orden.

    PUT /api/orders/{order_id}
    """
    repo = OrderRepository(db)

    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    updated = repo.update(order_id, data.model_dump(exclude_unset=True))
    return _enrich_order(updated)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina una orden.

    DELETE /api/orders/{order_id}
    """
    repo = OrderRepository(db)

    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden no encontrada",
        )

    repo.delete(order_id)
    return None
