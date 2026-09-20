# app/models/shippers.py
#
# Modelo ORM SQLAlchemy para la tabla "shippers".
#
# ============================================================================
# TABLA: shippers
# ============================================================================
# Descripcion: Transportistas que envian los pedidos.
#   Ej: Speedy Express, United Package, Federal Shipping.
#
# Columnas:
#   - shipper_id:    SMALLSERIAL PK, identificador unico del transportista
#   - company_name:  VARCHAR(40) NOT NULL, nombre de la empresa de envios
#   - phone:         VARCHAR(24) telefono de contacto
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   orders -> Order (1:N)
#     Un transportista puede enviar muchas ordenes.
#     La FK esta en orders.ship_via -> shippers.shipper_id.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener todos los transportistas:
#   transportistas = db.query(Shipper).all()
#
#   # Obtener un transportista con sus ordenes:
#   shipper = db.query(Shipper).options(
#       selectinload(Shipper.orders)
#   ).filter(Shipper.shipper_id == 1).first()
#
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Shipper(Base):
    __tablename__ = "shippers"

    shipper_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(String(40), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(24))

    # Relaciones
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="shipper",
    )

    def __repr__(self) -> str:
        return f"<Shipper {self.shipper_id}: {self.company_name}>"
