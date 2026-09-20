# app/models/suppliers.py
#
# Modelo ORM SQLAlchemy para la tabla "suppliers".
#
# ============================================================================
# TABLA: suppliers
# ============================================================================
# Descripcion: Proveedores de productos para Northwind.
#
# Columnas:
#   - supplier_id:    SMALLSERIAL PK, identificador unico del proveedor
#   - company_name:   VARCHAR(40) NOT NULL, nombre de la empresa proveedora
#   - contact_name:   VARCHAR(30) nombre del contacto
#   - contact_title:  VARCHAR(30) cargo del contacto
#   - address:        VARCHAR(60) direccion de la empresa
#   - city:           VARCHAR(15) ciudad
#   - region:         VARCHAR(15) region/estado
#   - postal_code:    VARCHAR(10) codigo postal
#   - country:        VARCHAR(15) pais
#   - phone:          VARCHAR(24) telefono de contacto
#   - fax:            VARCHAR(24) numero de fax
#   - homepage:       TEXT        URL del sitio web del proveedor
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   products -> Product (1:N)
#     Un proveedor puede suministrar muchos productos.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener todos los proveedores:
#   proveedores = db.query(Supplier).all()
#
#   # Obtener un proveedor con sus productos:
#   proveedor = db.query(Supplier).options(
#       selectinload(Supplier.products)
#   ).filter(Supplier.supplier_id == 1).first()
#
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
    homepage: Mapped[str | None] = mapped_column(Text)

    # Relaciones
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="supplier",
    )

    def __repr__(self) -> str:
        return f"<Supplier {self.supplier_id}: {self.company_name}>"
