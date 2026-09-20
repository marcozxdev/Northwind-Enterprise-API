# app/models/categories.py
#
# Modelo ORM SQLAlchemy para la tabla "categories".
#
# ============================================================================
# TABLA: categories
# ============================================================================
# Descripcion: Categorias de productos (ej: Beverages, Condiments, Seafood).
#
# Columnas:
#   - category_id:    SMALLSERIAL PK, identificador unico de la categoria
#   - category_name:  VARCHAR(15) NOT NULL, nombre de la categoria
#   - description:    TEXT        descripcion de la categoria
#   - picture:        BYTEA       imagen de la categoria (bytes)
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   products -> Product (1:N)
#     Una categoria contiene muchos productos.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener todas las categorias:
#   categorias = db.query(Category).all()
#
#   # Obtener una categoria con sus productos:
#   cat = db.query(Category).options(
#       selectinload(Category.products)
#   ).filter(Category.category_id == 1).first()
#
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(15), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    picture: Mapped[bytes | None] = mapped_column(default=None)

    # Relaciones
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return f"<Category {self.category_id}: {self.category_name}>"
