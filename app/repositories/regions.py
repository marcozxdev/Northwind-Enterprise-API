# app/repositories/regions.py
#
# Repository para los modelos Region y Territory.
#
# ============================================================================
# RegionRepository
# ============================================================================
#   Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
#
# ============================================================================
# TerritoryRepository
# ============================================================================
#   get_by_region(region_id):
#     - Lista territorios de una region especifica
#

from sqlalchemy.orm import Session

from app.models.regions import Region, Territory
from app.repositories.base import BaseRepository


class RegionRepository(BaseRepository[Region]):
    """
    Repository para el modelo Region.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Region, db)


class TerritoryRepository(BaseRepository[Territory]):
    """
    Repository para el modelo Territory.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Territory, db)

    def get_by_region(self, region_id: int) -> list[Territory]:
        """
        Lista territorios de una region.

        Args:
            region_id: ID de la region

        Returns:
            List[Territory]: Lista de territorios
        """
        return self.db.query(Territory).filter(
            Territory.region_id == region_id
        ).all()
