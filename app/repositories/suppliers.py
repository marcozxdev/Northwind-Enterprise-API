# app/repositories/suppliers.py
#
# Repository para el modelo Supplier.
#
# ============================================================================
# METODOS ESPECIFICOS
# ============================================================================
#
#   get_all_with_filters(country, city, company_name):
#     - Lista proveedores con filtros opcionales
#
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.suppliers import Supplier
from app.repositories.base import BaseRepository


class SupplierRepository(BaseRepository[Supplier]):
    """
    Repository para el modelo Supplier.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Supplier, db)

    def get_all_with_filters(
        self,
        page: int = 1,
        per_page: int = 10,
        country: Optional[str] = None,
        city: Optional[str] = None,
        company_name: Optional[str] = None,
    ) -> tuple[List[Supplier], int]:
        """
        Obtiene proveedores con filtros.

        Args:
            page: Pagina
            per_page: Registros por pagina
            country: Filtrar por pais
            city: Filtrar por ciudad
            company_name: Busqueda por nombre de empresa

        Returns:
            tuple: (lista de proveedores, total)
        """
        query = self.db.query(Supplier)

        if country:
            query = query.filter(Supplier.country.ilike(f"%{country}%"))
        if city:
            query = query.filter(Supplier.city.ilike(f"%{city}%"))
        if company_name:
            query = query.filter(Supplier.company_name.ilike(f"%{company_name}%"))

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return items, total
