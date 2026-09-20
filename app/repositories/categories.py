# app/repositories/categories.py
#
# Repository para el modelo Category.
#
# Hereda todas las operaciones CRUD del BaseRepository.
# Las categorias son pocas (8 registros en Northwind).
#
from sqlalchemy.orm import Session

from app.models.categories import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """
    Repository para el modelo Category.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Category, db)
