# app/schemas/users.py
#
# Esquemas Pydantic para el recurso Users (Usuarios) y autenticacion.
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de autenticacion y gestion de usuarios.
#
# ============================================================================
# ESQUEMAS DE AUTENTICACION
# ============================================================================
#
#   LoginRequest (POST /api/auth/login):
#     - username: str  [requerido, nombre de usuario]
#     - password: str  [requerido, contrasena en texto plano]
#
#   TokenResponse (respuesta del login):
#     - access_token: str   [token JWT generado]
#     - token_type:  str    [siempre "bearer"]
#     - expires_in:  int    [minutos hasta que expira]
#     - user:        UserResponse [datos del usuario autenticado]
#
#   RegisterRequest (POST /api/auth/register):
#     - username:  str  [requerido, min 3, max 50, unico]
#     - email:     str  [requerido, formato email, unico]
#     - password:  str  [requerido, min 6 caracteres]
#     - full_name: str  [opcional, nombre completo]
#
# ============================================================================
# ESQUEMAS DE USUARIO
# ============================================================================
#
#   UserResponse (respuesta estandar de usuario):
#     - user_id:    int
#     - username:   str
#     - email:      str
#     - full_name:  str | None
#     - is_active:  bool
#     - roles:      list[RoleResponse]
#     - created_at: datetime
#     - updated_at: datetime
#     - Config: from_attributes = True
#
#   UserUpdate (PUT /api/users/{id}):
#     - full_name: str | None  [opcional]
#     - email:     str | None  [opcional]
#
#   UserUpdateRoles (PUT /api/users/{id}/roles):
#     - role_ids: list[int]  [requerido, lista de role_ids a asignar]
#
#   UserList (respuesta paginada):
#     - items:    list[UserResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
# ============================================================================
# ESQUEMAS DE ROL
# ============================================================================
#
#   RoleResponse:
#     - role_id:     int
#     - role_name:   str
#     - description: str | None
#     - Config: from_attributes = True
#
#   RoleList:
#     - items: list[RoleResponse]
#     - total: int
#
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# ESQUEMAS DE AUTENTICACION
# ============================================================================


class LoginRequest(BaseModel):
    """
    Cuerpo del request para POST /api/auth/login

    Campos:
        - username: str [requerido, 3-50 caracteres]
        - password: str [requerido, minimo 6 caracteres]

    Ejemplo:
        {
            "username": "admin",
            "password": "admin123"
        }
    """
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    """
    Cuerpo del request para POST /api/auth/register

    Campos:
        - username:  str [requerido, 3-50 caracteres, unico]
        - email:     EmailStr [requerido, formato email, unico]
        - password:  str [requerido, 6-100 caracteres]
        - full_name: str | None [opcional, max 100 caracteres]
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)


class TokenResponse(BaseModel):
    """
    Respuesta del POST /api/auth/login

    Campos:
        - access_token: str [token JWT]
        - token_type:   str [siempre "bearer"]
        - expires_in:   int [minutos hasta expiracion]
        - user:         UserResponse [datos del usuario]
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"


# ============================================================================
# ESQUEMAS DE ROL
# ============================================================================


class RoleResponse(BaseModel):
    """
    Respuesta de un rol.

    Config:
        - from_attributes = True
    """
    role_id: int
    role_name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


class RoleList(BaseModel):
    """Respuesta de lista de roles."""
    items: list[RoleResponse]
    total: int


# ============================================================================
# ESQUEMAS DE USUARIO
# ============================================================================


class UserResponse(BaseModel):
    """
    Respuesta estandar de usuario (sin contraseña).

    Campos:
        - user_id:    int
        - username:   str
        - email:      str
        - full_name:  str | None
        - is_active:  bool
        - roles:      list[RoleResponse]
        - created_at: datetime
        - updated_at: datetime

    Config:
        - from_attributes = True
    """
    user_id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    roles: list[RoleResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """
    Cuerpo del request para PUT /api/users/{user_id}

    Campos (todos opcionales):
        - full_name: str | None
        - email:     EmailStr | None
    """
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None


class UserUpdateRoles(BaseModel):
    """
    Cuerpo del request para PUT /api/users/{user_id}/roles

    Campos:
        - role_ids: list[int] [requerido, lista de role_ids a asignar]
    """
    role_ids: list[int]


class UserList(BaseModel):
    """
    Respuesta paginada de usuarios.
    """
    items: list[UserResponse]
    total: int
    page: int
    per_page: int


# Actualizar referencia circular
TokenResponse.model_rebuild()
