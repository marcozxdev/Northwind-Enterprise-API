# app/models/customers.py
#
# Modelo ORM SQLAlchemy para la tabla "customers".
#
# ============================================================================
# TABLA: customers
# ============================================================================
# Descripcion: Clientes de la empresa Northwind.
#
# Columnas:
#   - customer_id:   VARCHAR(5)    PK, identificador unico (ej: "ALFKI")
#   - company_name:  VARCHAR(40)   NOT NULL, nombre de la empresa
#   - contact_name:  VARCHAR(30)   nombre del contacto principal
#   - contact_title: VARCHAR(30)   cargo del contacto
#   - address:       VARCHAR(60)   direccion de la empresa
#   - city:          VARCHAR(15)   ciudad
#   - region:        VARCHAR(15)   region/estado
#   - postal_code:   VARCHAR(10)   codigo postal
#   - country:       VARCHAR(15)   pais
#   - phone:         VARCHAR(24)   telefono de contacto
#   - fax:           VARCHAR(24)   numero de fax
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   orders -> Order (1:N)
#     Un cliente puede tener muchas ordenes.
#     Al eliminar un cliente, las ordenes se mantienen (SET NULL en customer_id).
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener todos los clientes:
#   clientes = db.query(Customer).all()
#
#   # Obtener un cliente con sus ordenes (eager loading):
#   cliente = db.query(Customer).options(
#       selectinload(Customer.orders)
#   ).filter(Customer.customer_id == "ALFKI").first()
#
#   # Crear un cliente:
#   nuevo = Customer(customer_id="NEW01", company_name="Mi Empresa")
#   db.add(nuevo)
#   db.commit()
#
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String(5), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(40), nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(30))
    contact_title: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(String(60))
    city: Mapped[str | None] = mapped_column(String(15))
    region: Mapped[str | None] = mapped_column(String(15))
    postal_code: Mapped[str | None] = mapped_column(String(10))
    country: Mapped[str | None] = mapped_column(String(15))
    phone: Mapped[str | None] = mapped_column(String(24))
    fax: Mapped[str | None] = mapped_column(String(24))

    # Relaciones
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Customer {self.customer_id}: {self.company_name}>"
