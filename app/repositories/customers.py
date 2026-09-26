# app/repositories/customers.py
#
# Repository para el modelo Customer.
#
# ============================================================================
# METODOS ESPECIFICOS
# ============================================================================
#
#   get_all_with_filters(company_name, city, country, contact_title):
#     - Lista clientes con filtros opcionales de busqueda
#
#   search(query):
#     - Busca clientes por company_name o contact_name
#

from sqlalchemy.orm import Session

from app.models.customers import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """
    Repository para el modelo Customer.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Customer, db)

    def get_all_with_filters(
        self,
        page: int = 1,
        per_page: int = 10,
        company_name: str | None = None,
        city: str | None = None,
        country: str | None = None,
        contact_title: str | None = None,
    ) -> tuple[list[Customer], int]:
        """
        Obtiene clientes con filtros opcionales.

        Args:
            page: Pagina actual
            per_page: Registros por pagina
            company_name: Busqueda parcial por nombre de empresa
            city: Filtrar por ciudad
            country: Filtrar por pais
            contact_title: Filtrar por cargo del contacto

        Returns:
            tuple: (lista de clientes, total)
        """
        query = self.db.query(Customer)

        if company_name:
            query = query.filter(Customer.company_name.ilike(f"%{company_name}%"))
        if city:
            query = query.filter(Customer.city.ilike(f"%{city}%"))
        if country:
            query = query.filter(Customer.country.ilike(f"%{country}%"))
        if contact_title:
            query = query.filter(Customer.contact_title.ilike(f"%{contact_title}%"))

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return items, total

    def search(self, query: str, page: int = 1, per_page: int = 10) -> tuple[list[Customer], int]:
        """
        Busca clientes por company_name o contact_name.

        Args:
            query: Texto a buscar
            page: Pagina
            per_page: Registros por pagina

        Returns:
            tuple: (lista de clientes, total)
        """
        search = f"%{query}%"
        query_obj = self.db.query(Customer).filter(
            (Customer.company_name.ilike(search))
            | (Customer.contact_name.ilike(search))
        )

        total = query_obj.count()
        items = query_obj.offset((page - 1) * per_page).limit(per_page).all()
        return items, total
