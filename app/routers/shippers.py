# app/routers/shippers.py
#
# Endpoints para el recurso Shippers (Transportistas).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/shippers          -> Listar transportistas
#   GET    /api/shippers/{id}     -> Obtener un transportista
#   POST   /api/shippers          -> Crear un transportista
#   PUT    /api/shippers/{id}     -> Actualizar un transportista
#   DELETE /api/shippers/{id}     -> Eliminar un transportista
#
# ============================================================================
# CACHE
# ============================================================================
#
#   GET endpoints usan Redis cache con TTL de 30 min (datos estaticos).
#   POST/PUT/DELETE invalidan el cache de shippers.
#
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.cache import cache_response, delete_cache_pattern
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.shippers import ShipperRepository
from app.schemas.shippers import (
    ShipperCreate,
    ShipperList,
    ShipperResponse,
    ShipperUpdate,
)

router = APIRouter(prefix="/shippers", tags=["Transportistas"])


@router.get("/", response_model=ShipperList)
@cache_response(ttl=1800, prefix="shippers:list")
def list_shippers(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista todos los transportistas.

    GET /api/shippers

    Cache: 1800 segundos (30 min) - datos estaticos.
    """
    repo = ShipperRepository(db)
    items, total = repo.get_all()
    return ShipperList(items=items, total=total)


@router.get("/{shipper_id}", response_model=ShipperResponse)
@cache_response(ttl=1800, prefix="shippers:get")
def get_shipper(
    shipper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene un transportista por ID.

    GET /api/shippers/{shipper_id}

    Cache: 1800 segundos (30 min) - datos estaticos.
    """
    repo = ShipperRepository(db)
    shipper = repo.get_by_id(shipper_id)

    if not shipper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transportista no encontrado",
        )

    return shipper


@router.post("/", response_model=ShipperResponse, status_code=status.HTTP_201_CREATED)
def create_shipper(
    data: ShipperCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea un nuevo transportista.

    POST /api/shippers

    Invalida cache de shippers.
    """
    repo = ShipperRepository(db)
    new_shipper = repo.create(data.model_dump())

    delete_cache_pattern("shippers:*")

    return new_shipper


@router.put("/{shipper_id}", response_model=ShipperResponse)
def update_shipper(
    shipper_id: int,
    data: ShipperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza un transportista.

    PUT /api/shippers/{shipper_id}

    Invalida cache de shippers.
    """
    repo = ShipperRepository(db)

    shipper = repo.get_by_id(shipper_id)
    if not shipper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transportista no encontrado",
        )

    updated = repo.update(shipper_id, data.model_dump(exclude_unset=True))

    delete_cache_pattern("shippers:*")

    return updated


@router.delete("/{shipper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipper(
    shipper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina un transportista.

    DELETE /api/shippers/{shipper_id}

    Invalida cache de shippers.
    """
    repo = ShipperRepository(db)

    shipper = repo.get_by_id(shipper_id)
    if not shipper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transportista no encontrado",
        )

    repo.delete(shipper_id)

    delete_cache_pattern("shippers:*")

    return None
