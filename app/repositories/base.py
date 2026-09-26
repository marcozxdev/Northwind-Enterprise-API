# app/repositories/base.py
#
# Repositorio base generico con operaciones CRUD comunes.
#
# Este modulo define una clase BaseRepository que proporciona
# las operaciones basicas de acceso a datos:
#   - get_by_id(): Buscar un registro por su ID
#   - get_all(): Listar todos los registros con paginacion
#   - create(): Crear un nuevo registro
#   - update(): Actualizar un registro existente
#   - delete(): Eliminar un registro
#   - count(): Contar total de registros
#
# ============================================================================
# USO
# ============================================================================
#
#   from app.repositories.base import BaseRepository
#   from app.models.customers import Customer
#
#   repo = BaseRepository(Customer, db)
#   customer = repo.get_by_id("ALFKI")
#   customers, total = repo.get_all(page=1, per_page=10)
#
# ============================================================================
# HERENCIA
# ============================================================================
#
#   Los repositories especificos heredan de esta clase:
#
#   class CustomerRepository(BaseRepository[Customer]):
#       def __init__(self, db):
#           super().__init__(Customer, db)
#
#       # Agregar metodos especificos...
#
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repositorio base generico con operaciones CRUD.

    Args:
        model: Clase del modelo SQLAlchemy
        db: Sesion de base de datos
    """

    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id_value) -> ModelType | None:
        """
        Obtiene un registro por su ID.

        Args:
            id_value: Valor del primary key

        Returns:
            ModelType | None: Registro encontrado o None
        """
        return self.db.query(self.model).filter(
            self.model.__table__.primary_key.columns[0] == id_value
        ).first()

    def get_all(self, page: int = 1, per_page: int = 10) -> tuple[list[ModelType], int]:
        """
        Obtiene todos los registros con paginacion.

        Args:
            page: Numero de pagina (default: 1)
            per_page: Registros por pagina (default: 10)

        Returns:
            tuple: (lista de registros, total de registros)
        """
        query = self.db.query(self.model)
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        return items, total

    def create(self, data: dict) -> ModelType:
        """
        Crea un nuevo registro.

        Args:
            data: Diccionario con los campos del registro

        Returns:
            ModelType: Registro creado con ID asignado
        """
        db_obj = self.model(**data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id_value, data: dict) -> ModelType | None:
        """
        Actualiza un registro existente.

        Args:
            id_value: Valor del primary key
            data: Diccionario con los campos a actualizar

        Returns:
            ModelType | None: Registro actualizado o None si no existe
        """
        db_obj = self.get_by_id(id_value)
        if db_obj:
            for key, value in data.items():
                setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj

    def delete(self, id_value) -> bool:
        """
        Elimina un registro.

        Args:
            id_value: Valor del primary key

        Returns:
            bool: True si se elimino, False si no existia
        """
        db_obj = self.get_by_id(id_value)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """
        Cuenta el total de registros.

        Returns:
            int: Numero total de registros
        """
        return self.db.query(self.model).count()
