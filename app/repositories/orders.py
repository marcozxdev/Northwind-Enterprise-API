# app/repositories/orders.py
#
# Repository para el modelo Order.
#
# ============================================================================
# METODOS ESPECIFICOS
# ============================================================================
#
#   get_with_details(order_id):
#     - Obtiene una orden con todos sus detalles, cliente, empleado y transportista
#
#   get_all_with_filters(customer_id, employee_id, date_from, date_to, shipped):
#     - Lista ordenes con filtros opcionales
#
#   create_with_details(order_data, details_data):
#     - Crea una orden con sus detalles en una sola transaccion
#
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session, selectinload

from app.models.orders import Order, OrderDetail
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository para el modelo Order.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Order, db)

    def get_with_details(self, order_id: int) -> Optional[Order]:
        """
        Obtiene una orden con todos sus detalles.

        Carga eagermente:
            - details (con product)
            - customer
            - employee
            - shipper

        Args:
            order_id: ID de la orden

        Returns:
            Order | None: Orden completa o None
        """
        return self.db.query(Order).options(
            selectinload(Order.details).selectinload(OrderDetail.product),
            selectinload(Order.customer),
            selectinload(Order.employee),
            selectinload(Order.shipper),
        ).filter(Order.order_id == order_id).first()

    def get_all_with_filters(
        self,
        page: int = 1,
        per_page: int = 10,
        customer_id: Optional[str] = None,
        employee_id: Optional[int] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        shipped: Optional[bool] = None,
    ) -> tuple[List[Order], int]:
        """
        Obtiene ordenes con filtros.

        Args:
            page: Pagina
            per_page: Registros por pagina
            customer_id: Filtrar por cliente
            employee_id: Filtrar por empleado
            date_from: Desde fecha
            date_to: Hasta fecha
            shipped: True=enviadas, False=pendientes

        Returns:
            tuple: (lista de ordenes, total)
        """
        query = self.db.query(Order).options(
            selectinload(Order.customer),
            selectinload(Order.employee),
            selectinload(Order.shipper),
        )

        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        if employee_id is not None:
            query = query.filter(Order.employee_id == employee_id)
        if date_from:
            query = query.filter(Order.order_date >= date_from)
        if date_to:
            query = query.filter(Order.order_date <= date_to)
        if shipped is not None:
            if shipped:
                query = query.filter(Order.shipped_date.isnot(None))
            else:
                query = query.filter(Order.shipped_date.is_(None))

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return items, total

    def create_with_details(self, order_data: dict, details_data: List[dict]) -> Order:
        """
        Crea una orden con sus detalles.

        Args:
            order_data: Datos de la orden
            details_data: Lista de detalles (product_id, unit_price, quantity, discount)

        Returns:
            Order: Orden creada con detalles
        """
        db_order = Order(**order_data)
        self.db.add(db_order)
        self.db.flush()

        for detail in details_data:
            db_detail = OrderDetail(order_id=db_order.order_id, **detail)
            self.db.add(db_detail)

        self.db.commit()
        self.db.refresh(db_order)
        return db_order
