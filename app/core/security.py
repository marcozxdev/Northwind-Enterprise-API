# app/core/security.py
#
# Funciones de seguridad para autenticación y autorización.
#
# Este módulo proporciona las herramientas necesarias para:
#   1. Hashear contraseñas con bcrypt
#   2. Verificar contraseñas contra hashes
#   3. Crear tokens JWT
#   4. Decodificar y validar tokens JWT
#
# ============================================================================
# FLUJO DE AUTENTICACIÓN
# ============================================================================
#
#   Registro:
#     1. Usuario envía password en texto plano
#     2. hash_password() genera un hash bcrypt
#     3. Se almacena solo el hash en la BD
#
#   Login:
#     1. Usuario envía password en texto plano
#     2. Se busca el usuario en la BD
#     3. verify_password() compara el password con el hash almacenado
#     4. Si coincide, se genera un token JWT
#
#   Uso del token:
#     1. El cliente envía el token en cada request
#     2. decode_access_token() extrae los datos del payload
#     3. Se usa el user_id del payload para buscar el usuario
#
# ============================================================================
# SEGURIDAD
# ============================================================================
#
#   - bcrypt genera un salt aleatorio para cada hash
#   - El hash incluye el salt, así que no necesitas guardarlo por separado
#   - JWT tiene una fecha de expiración configurada en settings.jwt
#   - El secret key para JWT está en las variables de entorno
#
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Convierte una contraseña en texto plano a su hash bcrypt.

    Args:
        password: Contraseña en texto plano (ej: "admin123")

    Returns:
        str: Hash bcrypt (ej: "$2b$12$LJ3m4...")

    Ejemplo:
        hashed = hash_password("mi_password")
        # "$2b$12$K0z8..."
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con un hash bcrypt.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash almacenado en la BD

    Returns:
        bool: True si coinciden, False si no

    Ejemplo:
        if verify_password("admin123", user.hashed_password):
            # Login exitoso
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT con los datos proporcionados.

    Args:
        data: Diccionario con los claims del token
              Ej: {"sub": "user_id", "roles": ["admin", "user"]}
        expires_delta: Tiempo de expiración (opcional, usa settings.jwt por defecto)

    Returns:
        str: Token JWT codificado

    Ejemplo:
        token = create_access_token({"sub": "1", "roles": ["admin"]})
        # "eyJhbGciOiJIUzI1NiIs..."
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXP_MIN)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT.

    Args:
        token: Token JWT a decodificar

    Returns:
        dict: Payload del token si es válido, None si no

    Ejemplo:
        payload = decode_access_token("eyJhbGciOiJIUzI1NiIs...")
        if payload:
            user_id = payload.get("sub")
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt.SECRET_KEY,
            algorithms=[settings.jwt.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
