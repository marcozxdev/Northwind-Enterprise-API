# app/routers/regions.py
#
# Endpoints para el recurso Regions (Regiones y Territorios).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/regions                  -> Listar regiones
#   GET    /api/regions/{id}             -> Obtener una region
#   GET    /api/regions/{id}/territories -> Territorios de una region
#   POST   /api/regions                  -> Crear una region
#   PUT    /api/regions/{id}             -> Actualizar una region
#   DELETE /api/regions/{id}             -> Eliminar una region
#   GET    /api/territories              -> Listar todos los territorios
#   GET    /api/territories/{id}         -> Obtener un territorio
#
# ============================================================================
# CACHE
# ============================================================================
#
#   GET endpoints usan Redis cache con TTL de 30 min (datos estaticos).
#   POST/PUT/DELETE invalidan el cache de regions/territories.
#
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.cache import cache_response, delete_cache_pattern
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.regions import RegionRepository, TerritoryRepository
from app.schemas.regions import (
    RegionCreate,
    RegionList,
    RegionResponse,
    RegionUpdate,
    TerritoryCreate,
    TerritoryResponse,
    TerritoryUpdate,
)

router = APIRouter(tags=["Regiones"])


# ============================================================================
# REGIONES
# ============================================================================


@router.get("/regions", response_model=RegionList)
@cache_response(ttl=1800, prefix="regions:list")
def list_regions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista todas las regiones.

    GET /api/regions

    Cache: 1800 segundos (30 min) - datos estaticos.
    """
    repo = RegionRepository(db)
    items, total = repo.get_all()
    return RegionList(items=items, total=total)


@router.get("/regions/{region_id}", response_model=RegionResponse)
@cache_response(ttl=1800, prefix="regions:get")
def get_region(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene una region por ID.

    GET /api/regions/{region_id}

    Cache: 1800 segundos (30 min) - datos estaticos.
    """
    repo = RegionRepository(db)
    region = repo.get_by_id(region_id)

    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region no encontrada",
        )

    return region


@router.get("/regions/{region_id}/territories", response_model=list[TerritoryResponse])
def list_region_territories(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista los territorios de una region.

    GET /api/regions/{region_id}/territories
    """
    region_repo = RegionRepository(db)
    territory_repo = TerritoryRepository(db)

    region = region_repo.get_by_id(region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region no encontrada",
        )

    territories = territory_repo.get_by_region(region_id)
    return territories


@router.post("/regions", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
def create_region(
    data: RegionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea una nueva region.

    POST /api/regions

    Invalida cache de regions.
    """
    repo = RegionRepository(db)
    new_region = repo.create(data.model_dump())

    delete_cache_pattern("regions:*")

    return new_region


@router.put("/regions/{region_id}", response_model=RegionResponse)
def update_region(
    region_id: int,
    data: RegionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza una region.

    PUT /api/regions/{region_id}

    Invalida cache de regions.
    """
    repo = RegionRepository(db)

    region = repo.get_by_id(region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region no encontrada",
        )

    updated = repo.update(region_id, data.model_dump(exclude_unset=True))

    delete_cache_pattern("regions:*")

    return updated


@router.delete("/regions/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_region(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina una region.

    DELETE /api/regions/{region_id}

    Invalida cache de regions.
    """
    repo = RegionRepository(db)

    region = repo.get_by_id(region_id)
    if not region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region no encontrada",
        )

    repo.delete(region_id)

    delete_cache_pattern("regions:*")

    return None


# ============================================================================
# TERRITORIOS
# ============================================================================


@router.get("/territories", response_model=list[TerritoryResponse])
@cache_response(ttl=1800, prefix="territories:list")
def list_territories(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista todos los territorios.

    GET /api/territories

    Cache: 1800 segundos (30 min) - datos estaticos.
    """
    repo = TerritoryRepository(db)
    items, _ = repo.get_all()
    return items


@router.get("/territories/{territory_id}", response_model=TerritoryResponse)
@cache_response(ttl=1800, prefix="territories:get")
def get_territory(
    territory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene un territorio por ID.

    GET /api/territories/{territory_id}

    Cache: 1800 segundos (30 min) - datos estaticos.
    """
    repo = TerritoryRepository(db)
    territory = repo.get_by_id(territory_id)

    if not territory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Territorio no encontrado",
        )

    return territory


@router.post("/territories", response_model=TerritoryResponse, status_code=status.HTTP_201_CREATED)
def create_territory(
    data: TerritoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea un nuevo territorio.

    POST /api/territories

    Invalida cache de territories.
    """
    repo = TerritoryRepository(db)

    existing = repo.get_by_id(data.territory_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un territorio con ese ID",
        )

    new_territory = repo.create(data.model_dump())

    delete_cache_pattern("territories:*")

    return new_territory


@router.put("/territories/{territory_id}", response_model=TerritoryResponse)
def update_territory(
    territory_id: str,
    data: TerritoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza un territorio.

    PUT /api/territories/{territory_id}

    Invalida cache de territories.
    """
    repo = TerritoryRepository(db)

    territory = repo.get_by_id(territory_id)
    if not territory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Territorio no encontrado",
        )

    updated = repo.update(territory_id, data.model_dump(exclude_unset=True))

    delete_cache_pattern("territories:*")

    return updated


@router.delete("/territories/{territory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_territory(
    territory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina un territorio.

    DELETE /api/territories/{territory_id}

    Invalida cache de territories.
    """
    repo = TerritoryRepository(db)

    territory = repo.get_by_id(territory_id)
    if not territory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Territorio no encontrado",
        )

    repo.delete(territory_id)

    delete_cache_pattern("territories:*")

    return None
