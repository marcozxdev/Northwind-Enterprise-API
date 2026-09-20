# app/models/products.py
#
# Modelo ORM SQLAlchemy para la tabla "products".
#
# ============================================================================
# TABLA: products
# ============================================================================
# Descripcion: Productos que vende la empresa Northwind.
#
# Columnas:
#   - product_id:         SMALLSERIAL PK, identificador unico del producto
#   - product_name:       VARCHAR(40) NOT NULL, nombre del producto
#   - supplier_id:        SMALLINT    FK -> suppliers.supplier_id
#   - category_id:        SMALLINT    FK -> categories.category_id
#   - quantity_per_unit:  VARCHAR(20) descripcion de la unidad
#   - unit_price:         REAL        precio unitario de venta
#   - units_in_stock:     SMALLINT    unidades disponibles en inventario
#   - units_on_order:     SMALLINT    unidades pedidas al proveedor
#   - reorder_level:      SMALLINT    nivel minimo de stock para reordenar
#   - discontinued:       INTEGER     0 = activo, 1 = descontinuado
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   category -> Category (N:1)
#     Un producto pertenece a una categoria.
#     FK: products.category_id -> categories.category_id
#
#   supplier -> Supplier (N:1)
#     Un producto es suministrado por un proveedor.
#     FK: products.supplier_id -> suppliers.supplier_id
#
#   order_details -> OrderDetail (1:N)
#     Un producto puede aparecer en muchos detalles de orden.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener productos con categoria y proveedor (eager loading):
#   productos = db.query(Product).options(
#       selectinload(Product.category),
#       selectinload(Product.supplier),
#   ).all()
#
#   # Obtener un producto con sus detalles de orden:
#   producto = db.query(Product).options(
#       selectinload(Product.order_details)
#   ).filter(Product.product_id == 1).first()
#
#   # Filtrar solo productos activos (no descontinuados):
#   activos = db.query(Product).filter(Product.discontinued == 0).all()
#
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(40), nullable=False)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.supplier_id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.category_id"))
    quantity_per_unit: Mapped[str | None] = mapped_column(String(20))
    unit_price: Mapped[float | None] = mapped_column()
    units_in_stock: Mapped[int | None] = mapped_column()
    units_on_order: Mapped[int | None] = mapped_column()
    reorder_level: Mapped[int | None] = mapped_column()
    discontinued: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relaciones
    category: Mapped["Category | None"] = relationship(
        "Category",
        back_populates="products",
    )
    supplier: Mapped["Supplier | None"] = relationship(
        "Supplier",
        back_populates="products",
    )
    order_details: Mapped[list["OrderDetail"]] = relationship(
        "OrderDetail",
        back_populates="product",
    )

    def __repr__(self) -> str:
        return f"<Product {self.product_id}: {self.product_name}>"
