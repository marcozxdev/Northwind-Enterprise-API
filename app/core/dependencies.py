# app/core/dependencies.py
#
# Dependencias inyectables para los endpoints de FastAPI.
#
# FastAPI permite inyectar dependencias en los parametros de los endpoints
# usando Depends(). Este archivo centraliza las dependencias comunes,
# especialmente las de autenticacion y autorizacion.
#
# ============================================================================
# FLUJO DE AUTENTICACION
# ============================================================================
#
#   1. El cliente envia un request con header: Authorization: Bearer <token>
#   2. OAuth2PasswordBearer extrae el token del header.
#   3. get_current_user() decodifica el JWT y retorna el usuario.
#   4. get_current_active_user() verifica que el usuario este activo.
#   5. require_role("admin") verifica que el usuario tenga el rol necesario.
#
# ============================================================================
# DEPENDENCIAS
# ============================================================================
#
#   get_db():
#     - Obtiene una sesion de BD y la cierra al finalizar el request.
#     - Se usa en cada endpoint que necesite acceder a la BD.
#
#   oauth2_scheme:
#     - Instancia de OAuth2PasswordBearer que apunta a /api/auth/login.
#     - Extrae el token del header Authorization automaticamente.
#
#   get_current_user(token, db):
#     - Decodifica el token JWT usando la clave secreta.
#     - Busca el usuario en la BD por el user_id del token.
#     - Retorna el objeto User de la BD.
#     - Lanza HTTPException(401) si el token es invalido o el usuario no existe.
#
#   get_current_active_user(current_user):
#     - Verifica que el campo is_active del usuario sea True.
#     - Lanza HTTPException(403) si el usuario esta desactivado.
#
#   require_role(roles):
#     - Factory que retorna una dependencia que verifica el rol del usuario.
#     - Recibe una lista de roles permitidos.
#     - Lanza HTTPException(403) si el usuario no tiene ninguno de los roles.
#
# ============================================================================
# EJEMPLO DE USO EN UN ENDPOINT
# ============================================================================
#
#   @router.get("/me")
#   def perfil_usuario(current_user: User = Depends(get_current_active_user)):
#       return current_user
#
#   @router.delete("/users/{user_id}")
#   def eliminar_usuario(
#       user_id: int,
#       db: Session = Depends(get_db),
#       current_user: User = Depends(require_role(["admin"]))
#   ):
#       ...
#
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.users import User

# Instancia de HTTPBearer que extrae el token del header Authorization
# FastAPI usará esto para extraer el token del header
# Swagger mostrara un campo simple para pegar el token JWT
oauth2_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual a partir del token JWT.

    Args:
        credentials: Credenciales extraídas del header Authorization
        db: Sesión de base de datos

    Returns:
        User: Objeto usuario de la BD

    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario actual esté activo.

    Args:
        current_user: Usuario obtenido del token

    Returns:
        User: Usuario si está activo

    Raises:
        HTTPException 403: Si el usuario está desactivado
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )
    return current_user


def require_role(allowed_roles: list[str]):
    """
    Factory que retorna una dependencia que verifica roles.

    Args:
        allowed_roles: Lista de roles permitidos
                      Ej: ["admin"], ["admin", "user"]

    Returns:
        Callable: Dependencia que verifica el rol

    Uso en endpoint:
        @router.delete("/users/{user_id}")
        def eliminar(
            user_id: int,
            current_user = Depends(require_role(["admin"]))
        ):
            ...
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        user_roles = [role.role_name for role in current_user.roles]

        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de estos roles: {', '.join(allowed_roles)}"
            )

        return current_user

    return role_checker
