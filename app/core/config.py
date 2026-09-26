# app/config.py
#
# Configuracion centralizada de la aplicacion.
#
# Usa pydantic-settings para leer variables de entorno desde el archivo .env.
# Si no existe .env, usa los valores por defecto definidos aqui.
#
# Uso:
#   from app.config import settings
#   settings.db.DATABASE_URL
#   settings.jwt.JWT_SECRET_KEY
#

import logging
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Valores que nunca deben usarse para firmar tokens en produccion.
INSECURE_JWT_SECRETS = frozenset({
    "",
    "YOUR-SECRET-key",
    "CHANGE-THIS-TO-A-SECRET-KEY",
    "changeme",
})


class AppConfig(BaseSettings):
    """Configuracion general de la aplicacion."""
    model_config = SettingsConfigDict(env_prefix="APP_")

    NAME: str = "Northwind Enterprise API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True


class DatabaseConfig(BaseSettings):
    """Configuracion de conexion a PostgreSQL."""
    model_config = SettingsConfigDict(env_prefix="DB_")

    USER: str = "northwind_user"
    PASSWORD: str = "northwind_password"
    NAME: str = "northwind"
    HOST: str = "northwind_postgres"
    PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class RedisConfig(BaseSettings):
    """Configuracion de conexion a Redis."""
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    HOST: str = "northwind_redis"
    PORT: int = 6379

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}/0"


class CORSSettings(BaseSettings):
    """Origenes permitidos por CORS.

    Pydantic-settings parsea las listas desde variables de entorno como JSON,
    por lo que en el .env se define un unico valor con formato de lista:

        CORS_ORIGINS=["http://localhost:3000","https://miapp.com"]

    Nunca se debe combinar "*" con allow_credentials=True: el navegador
    rechaza credenciales cuando el origen es comodin, y proxies
    intermedios como nginx terminan aceptandolo igualmente, dejando la
    API abierta.
    """
    model_config = SettingsConfigDict(env_prefix="CORS_")

    ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    ALLOW_HEADERS: list[str] = ["Authorization", "Content-Type", "Accept"]

    @model_validator(mode="after")
    def _reject_wildcard_with_credentials(self) -> "CORSSettings":
        """Impide la combinacion insegura de comodin + credenciales."""
        if "*" in self.ORIGINS and self.ALLOW_CREDENTIALS:
            raise ValueError(
                "CORS_ORIGINS no puede contener '*' mientras "
                "CORS_ALLOW_CREDENTIALS sea True. Define los origins "
                "explicitamente en el .env."
            )
        return self


class JWTConfig(BaseSettings):
    """Configuracion de autenticacion JWT."""
    model_config = SettingsConfigDict(env_prefix="JWT_")

    SECRET_KEY: str = "YOUR-SECRET-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXP_MIN: int = 40

    @property
    def is_insecure(self) -> bool:
        """True si la clave sigue siendo un valor de ejemplo."""
        return self.SECRET_KEY.strip() in INSECURE_JWT_SECRETS


class Settings(BaseSettings):
    """Configuracion principal que agrupa todos los grupos."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    jwt: JWTConfig = JWTConfig()
    cors: CORSSettings = CORSSettings()

    @model_validator(mode="after")
    def _guard_secret_in_production(self) -> "Settings":
        """Impide arrancar en produccion con la clave de ejemplo.

        En DEBUG se permite arrancar para que el proyecto funcione con un
        `cp .env.example .env`, pero se emite una advertencia visible. Con
        DEBUG=False la clave de ejemplo aborta el arranque: un token firmado
        con una clave publica del repositorio es equivalente a no tener auth.
        """
        if self.jwt.is_insecure:
            if not self.app.DEBUG:
                raise ValueError(
                    "JWT_SECRET_KEY sigue siendo un valor de ejemplo y la "
                    "aplicacion no esta en DEBUG. Genera una clave real, por "
                    "ejemplo: python -c \"import secrets;"
                    "print(secrets.token_urlsafe(64))\""
                )
            logging.getLogger(__name__).warning(
                "JWT_SECRET_KEY usa un valor de ejemplo. Esto es aceptable "
                "solo en desarrollo; nunca despliegues asi."
            )
        return self


@lru_cache
def get_settings() -> Settings:
    """Retorna una instancia cacheada de Settings."""
    return Settings()


settings = get_settings()
