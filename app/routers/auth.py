# app/routers/auth.py
#
# Endpoints de autenticacion y gestion de usuarios.
#
# Este router maneja el ciclo de vida completo de autenticacion:
#   - Registro de nuevos usuarios
#   - Login y generacion de tokens JWT
#   - Obtener perfil del usuario autenticado
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   POST /api/auth/register
#     - Registra un nuevo usuario en el sistema.
#     - Body: RegisterRequest (username, email, password, full_name)
#     - Retorna: UserResponse (sin contrasena)
#     - Flujo:
#         1. Validar que username y email no existan.
#         2. Hashear la contrasena con bcrypt.
#         3. Crear el usuario en la BD.
#         4. Asignar rol "viewer" por defecto.
#         5. Retornar el usuario creado.
#
#   POST /api/auth/login
#     - Autentica un usuario y retorna un token JWT.
#     - Body: LoginRequest (username, password)
#     - Retorna: TokenResponse (access_token, token_type, expires_in, user)
#     - Flujo:
#         1. Buscar el usuario por username.
#         2. Verificar el hash bcrypt contra la contrasena.
#         3. Si es correcto, generar token JWT con user_id y roles.
#         4. Retornar el token y datos del usuario.
#
#   GET /api/auth/me
#     - Retorna el perfil del usuario autenticado.
#     - Requiere: Header Authorization con token JWT valido.
#     - Retorna: UserResponse con roles incluidos.
#
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.core.security import create_access_token, hash_password, verify_password
from app.models.roles import Role
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.

    POST /api/auth/register

    Body:
        - username:  str [requerido]
        - email:     EmailStr [requerido]
        - password:  str [requerido, min 6]
        - full_name: str | None [opcional]

    Response:
        201: UserResponse (sin contrasena)

    Flujo:
        1. Verificar que username no exista
        2. Verificar que email no exista
        3. Hashear la contrasena
        4. Crear usuario con rol "viewer" por defecto
        5. Retornar usuario creado
    """
    repo = UserRepository(db)

    # Verificar username unico
    if repo.get_by_username(data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya esta en uso",
        )

    # Verificar email unico
    if repo.get_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya esta registrado",
        )

    # Hashear contrasena
    hashed_pw = hash_password(data.password)

    # Obtener rol viewer por defecto
    viewer_role = db.query(Role).filter(Role.role_name == "viewer").first()
    role_ids = [viewer_role.role_id] if viewer_role else []

    # Crear usuario
    user_data = data.model_dump()
    user_data["hashed_password"] = hashed_pw
    del user_data["password"]

    new_user = repo.create_with_roles(user_data, role_ids)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Inicia sesion y retorna un token JWT.

    POST /api/auth/login

    Body:
        - username: str
        - password: str

    Response:
        200: TokenResponse
        {
            "access_token": "eyJ...",
            "token_type": "bearer",
            "expires_in": 40,
            "user": { ... }
        }
    """
    repo = UserRepository(db)
    user = repo.get_by_username(data.username)

    # Verificar usuario existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    # Verificar contrasena
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    # Verificar que este activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada",
        )

    # Generar token JWT
    token_data = {"sub": str(user.user_id), "roles": user.role_names}
    access_token = create_access_token(token_data)

    return TokenResponse(
        access_token=access_token,
        expires_in=40,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Retorna el perfil del usuario autenticado.

    GET /api/auth/me

    Headers:
        Authorization: Bearer <token>

    Response:
        200: UserResponse con roles
    """
    return current_user
