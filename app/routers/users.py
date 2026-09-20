# app/routers/users.py
#
# Endpoints de gestion de usuarios (solo administradores).
#
# Todos los endpoints requieren autenticacion y rol "admin".
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET /api/users
#     - Lista todos los usuarios (paginado).
#     - Requiere: Rol "admin".
#     - Query params: page, per_page, search
#
#   GET /api/users/{user_id}
#     - Obtiene un usuario por ID.
#     - Requiere: Rol "admin".
#
#   PUT /api/users/{user_id}
#     - Actualiza datos de un usuario.
#     - Requiere: Rol "admin".
#     - Body: UserUpdate (full_name, email)
#
#   DELETE /api/users/{user_id}
#     - Desactiva un usuario (soft delete).
#     - Requiere: Rol "admin".
#
#   PUT /api/users/{user_id}/roles
#     - Asigna roles a un usuario.
#     - Requiere: Rol "admin".
#     - Body: UserUpdateRoles (role_ids: list[int])
#
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserList, UserResponse, UserUpdate, UserUpdateRoles

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/", response_model=UserList)
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Lista todos los usuarios (solo admin).

    GET /api/users?page=1&per_page=10&search=juan
    """
    repo = UserRepository(db)

    if search:
        items, total = repo.search(search, page, per_page)
    else:
        items, total = repo.get_all_with_roles(page, per_page)

    return UserList(items=items, total=total, page=page, per_page=per_page)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Obtiene un usuario por ID.

    GET /api/users/{user_id}
    """
    repo = UserRepository(db)
    user = repo.get_with_roles(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Actualiza datos de un usuario.

    PUT /api/users/{user_id}
    """
    repo = UserRepository(db)

    user = repo.get_with_roles(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    # Verificar email unico si se esta cambiando
    if data.email and data.email != user.email:
        existing = repo.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya esta en uso",
            )

    updated = repo.update(user_id, data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Desactiva un usuario (soft delete).

    DELETE /api/users/{user_id}
    """
    repo = UserRepository(db)

    # No permitir desactivarse a si mismo
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes desactivar tu propia cuenta",
        )

    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    repo.update(user_id, {"is_active": False})
    return None


@router.put("/{user_id}/roles", response_model=UserResponse)
def update_user_roles(
    user_id: int,
    data: UserUpdateRoles,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Asigna roles a un usuario (reemplaza los existentes).

    PUT /api/users/{user_id}/roles
    """
    repo = UserRepository(db)

    user = repo.get_with_roles(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    updated = repo.update_roles(user_id, data.role_ids)
    return updated
