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

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class JWTConfig(BaseSettings):
    """Configuracion de autenticacion JWT."""
    model_config = SettingsConfigDict(env_prefix="JWT_")

    SECRET_KEY: str = "YOUR-SECRET-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXP_MIN: int = 40


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


@lru_cache()
def get_settings() -> Settings:
    """Retorna una instancia cacheada de Settings."""
    return Settings()


settings = get_settings()
