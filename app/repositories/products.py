# app/repositories/products.py
#
# Repository para el modelo Product.
#
# ============================================================================
# METODOS ESPECIFICOS
# ============================================================================
#
#   get_with_relations(product_id):
#     - Obtiene un producto con category y supplier (eager loading)
#
#   get_all_with_filters(category_id, supplier_id, discontinued, price_min, price_max, in_stock):
#     - Lista productos con filtros opcionales
#

from sqlalchemy.orm import Session, selectinload

from app.models.products import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository para el modelo Product.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_with_relations(self, product_id: int) -> Product | None:
        """
        Obtiene un producto con categoria y proveedor.

        Args:
            product_id: ID del producto

        Returns:
            Product | None: Producto con relaciones o None
        """
        return self.db.query(Product).options(
            selectinload(Product.category),
            selectinload(Product.supplier),
        ).filter(Product.product_id == product_id).first()

    def get_all_with_filters(
        self,
        page: int = 1,
        per_page: int = 10,
        category_id: int | None = None,
        supplier_id: int | None = None,
        discontinued: bool | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        in_stock: bool | None = None,
    ) -> tuple[list[Product], int]:
        """
        Obtiene productos con filtros.

        Args:
            page: Pagina
            per_page: Registros por pagina
            category_id: Filtrar por categoria
            supplier_id: Filtrar por proveedor
            discontinued: True=solo activos, False=solo descontinuados
            price_min: Precio minimo
            price_max: Precio maximo
            in_stock: True=solo con stock > 0

        Returns:
            tuple: (lista de productos con category_name y supplier_company, total)
        """
        query = self.db.query(Product).options(
            selectinload(Product.category),
            selectinload(Product.supplier),
        )

        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        if supplier_id is not None:
            query = query.filter(Product.supplier_id == supplier_id)
        if discontinued is not None:
            discontinued_val = 1 if discontinued else 0
            query = query.filter(Product.discontinued == discontinued_val)
        if price_min is not None:
            query = query.filter(Product.unit_price >= price_min)
        if price_max is not None:
            query = query.filter(Product.unit_price <= price_max)
        if in_stock:
            query = query.filter(Product.units_in_stock > 0)

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return items, total
