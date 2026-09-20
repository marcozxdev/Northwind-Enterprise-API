# app/models/orders.py
#
# Modelos ORM SQLAlchemy para las tablas "orders" y "order_details".
#
# ============================================================================
# TABLA: orders
# ============================================================================
# Descripcion: Ordenes de compra realizadas por los clientes.
#
# Columnas:
#   - order_id:          SMALLSERIAL PK, identificador unico de la orden
#   - customer_id:       VARCHAR(5)  FK -> customers.customer_id
#   - employee_id:       SMALLINT    FK -> employees.employee_id
#   - order_date:        DATE        fecha en que se registro la orden
#   - required_date:     DATE        fecha en que se requiere la entrega
#   - shipped_date:      DATE        fecha en que se envio
#   - ship_via:          SMALLINT    FK -> shippers.shipper_id (transportista)
#   - freight:           REAL        costo total del flete
#   - ship_name:         VARCHAR(40) nombre para el envio
#   - ship_address:      VARCHAR(60) direccion de envio
#   - ship_city:         VARCHAR(15) ciudad de envio
#   - ship_region:       VARCHAR(15) region de envio
#   - ship_postal_code:  VARCHAR(10) codigo postal de envio
#   - ship_country:      VARCHAR(15) pais de envio
#
# ============================================================================
# RELACIONES (orders)
# ============================================================================
#
#   customer -> Customer (N:1)
#     Una orden pertenece a un cliente.
#     FK: orders.customer_id -> customers.customer_id
#
#   employee -> Employee (N:1)
#     Una orden fue tomada por un empleado.
#     FK: orders.employee_id -> employees.employee_id
#
#   shipper -> Shipper (N:1)
#     Una orden fue enviada por un transportista.
#     FK: orders.ship_via -> shippers.shipper_id
#
#   details -> OrderDetail (1:N)
#     Una orden tiene muchos detalles (line items).
#
# ============================================================================
# TABLA: order_details
# ============================================================================
# Descripcion: Detalles (line items) de cada orden.
#
# Columnas:
#   - order_id:    SMALLINT PK, FK -> orders.order_id
#   - product_id:  SMALLINT PK, FK -> products.product_id
#   - unit_price:  REAL     precio unitario al momento de la compra
#   - quantity:    SMALLINT cantidad ordenada
#   - discount:    REAL     descuento aplicado (0 a 1)
#
# Nota: La PK es compuesta (order_id, product_id).
#
# ============================================================================
# RELACIONES (order_details)
# ============================================================================
#
#   order -> Order (N:1)
#     Un detalle pertenece a una orden.
#
#   product -> Product (N:1)
#     Un detalle corresponde a un producto.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener ordenes con cliente, empleado y transportista:
#   ordenes = db.query(Order).options(
#       selectinload(Order.customer),
#       selectinload(Order.employee),
#       selectinload(Order.shipper),
#   ).all()
#
#   # Obtener una orden con todos sus detalles:
#   orden = db.query(Order).options(
#       selectinload(Order.details).selectinload(OrderDetail.product)
#   ).filter(Order.order_id == 10248).first()
#   # orden.details[0].product.product_name -> "Queso Cabrales"
#
#   # Crear una orden con detalles:
#   nueva_orden = Order(
#       customer_id="ALFKI",
#       employee_id=5,
#       order_date=date.today(),
#       details=[
#           OrderDetail(product_id=1, unit_price=14.0, quantity=12, discount=0),
#           OrderDetail(product_id=42, unit_price=9.8, quantity=10, discount=0),
#       ]
#   )
#   db.add(nueva_orden)
#   db.commit()
#
from datetime import date
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[str | None] = mapped_column(
        ForeignKey("customers.customer_id")
    )
    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.employee_id")
    )
    order_date: Mapped[date | None] = mapped_column()
    required_date: Mapped[date | None] = mapped_column()
    shipped_date: Mapped[date | None] = mapped_column()
    ship_via: Mapped[int | None] = mapped_column(ForeignKey("shippers.shipper_id"))
    freight: Mapped[float | None] = mapped_column()
    ship_name: Mapped[str | None] = mapped_column(String(40))
    ship_address: Mapped[str | None] = mapped_column(String(60))
    ship_city: Mapped[str | None] = mapped_column(String(15))
    ship_region: Mapped[str | None] = mapped_column(String(15))
    ship_postal_code: Mapped[str | None] = mapped_column(String(10))
    ship_country: Mapped[str | None] = mapped_column(String(15))

    # Relaciones
    customer: Mapped["Customer | None"] = relationship(
        "Customer",
        back_populates="orders",
    )
    employee: Mapped["Employee | None"] = relationship(
        "Employee",
        back_populates="orders",
    )
    shipper: Mapped["Shipper | None"] = relationship(
        "Shipper",
        back_populates="orders",
    )
    details: Mapped[list["OrderDetail"]] = relationship(
        "OrderDetail",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Order {self.order_id}>"


class OrderDetail(Base):
    __tablename__ = "order_details"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.order_id"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id"), primary_key=True
    )
    unit_price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    discount: Mapped[float] = mapped_column(nullable=False, default=0)

    # Relaciones
    order: Mapped["Order"] = relationship("Order", back_populates="details")
    product: Mapped["Product"] = relationship("Product", back_populates="order_details")

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal: unit_price * quantity * (1 - discount)"""
        return self.unit_price * self.quantity * (1 - self.discount)

    def __repr__(self) -> str:
        return f"<OrderDetail order={self.order_id} product={self.product_id}>"
