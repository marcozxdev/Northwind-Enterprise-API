# app/repositories/shippers.py
#
# Repository para el modelo Shipper.
#
# Hereda todas las operaciones CRUD del BaseRepository.
# Son pocos registros (3 en Northwind: Speedy Express, United Package, Federal Shipping).
#
from sqlalchemy.orm import Session

from app.models.shippers import Shipper
from app.repositories.base import BaseRepository


class ShipperRepository(BaseRepository[Shipper]):
    """
    Repository para el modelo Shipper.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Shipper, db)
