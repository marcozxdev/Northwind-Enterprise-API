# app/core/cache.py
#
# Modulo de cache con Redis.
#
# Este modulo proporciona funciones y un decorator para cachear
# respuestas de endpoints en Redis, reduciendo la latencia y
# la carga sobre PostgreSQL.
#
# ============================================================================
# FUNCIONES
# ============================================================================
#
#   get_redis_client():
#     - Retorna la instancia global de Redis.
#     - Se inicializa en startup de main.py.
#
#   init_redis():
#     - Crea la conexion a Redis al arrancar la app.
#
#   close_redis():
#     - Cierra la conexion al apagar la app.
#
#   get_cache(key):
#     - Obtiene un valor del cache por su key.
#     - Retorna dict | None.
#
#   set_cache(key, value, ttl):
#     - Guarda un valor en el cache con TTL en segundos.
#
#   delete_cache_pattern(pattern):
#     - Elimina todas las keys que coincidan con el patron.
#     - Se usa para invalidacion (ej: "products:*").
#
#   build_cache_key(prefix, **kwargs):
#     - Construye una key de cache con prefijo y parametros.
#     - Ej: "products:list:1:10:abc123"
#
# ============================================================================
# DECORATOR
# ============================================================================
#
#   @cache_response(ttl=300, prefix="products")
#     - Cachea automaticamente la respuesta de un endpoint GET.
#     - Si hay cache hit, retorna el valor cacheado.
#     - Si hay cache miss, ejecuta el endpoint y guarda el resultado.
#
# ============================================================================
# FLUJO DE USO EN ROUTERS
# ============================================================================
#
#   @router.get("/", response_model=ProductList)
#   @cache_response(ttl=180, prefix="products")
#   def list_products(...):
#       ...
#
#   @router.get("/{product_id}", response_model=ProductResponse)
#   @cache_response(ttl=300, prefix="products")
#   def get_product(...):
#       ...
#
#   @router.post("/", response_model=ProductResponse, status_code=201)
#   def create_product(...):
#       new_product = repo.create(...)
#       delete_cache_pattern("products:*")  # Invalidar cache
#       return new_product
#
import hashlib
import json
import logging
from functools import wraps
from typing import Any, Optional

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

# Instancia global de Redis
_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """
    Retorna la instancia global de Redis.

    Returns:
        redis.Redis | None: Cliente Redis o None si no esta disponible.
    """
    return _redis_client


def init_redis() -> redis.Redis:
    """
    Inicializa la conexion a Redis.

    Se llama en el startup event de FastAPI.

    Returns:
        redis.Redis: Cliente Redis conectado.
    """
    global _redis_client

    try:
        _redis_client = redis.Redis(
            host=settings.redis.HOST,
            port=settings.redis.PORT,
            db=0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        # Verificar conexion
        _redis_client.ping()
        logger.info("Redis connected at %s:%s", settings.redis.HOST, settings.redis.PORT)
        return _redis_client
    except redis.ConnectionError as e:
        logger.warning("Redis connection failed: %s. Cache disabled.", e)
        _redis_client = None
        return None
    except Exception as e:
        logger.warning("Redis init error: %s. Cache disabled.", e)
        _redis_client = None
        return None


def close_redis():
    """
    Cierra la conexion a Redis.

    Se llama en el shutdown event de FastAPI.
    """
    global _redis_client
    if _redis_client:
        try:
            _redis_client.close()
            logger.info("Redis connection closed.")
        except Exception as e:
            logger.warning("Error closing Redis: %s", e)
        _redis_client = None


def get_cache(key: str) -> Optional[Any]:
    """
    Obtiene un valor del cache por su key.

    Args:
        key: Clave del cache (ej: "products:list:1:10")

    Returns:
        dict | list | None: Valor cacheado o None si no existe.
    """
    client = get_redis_client()
    if not client:
        return None

    try:
        value = client.get(key)
        if value:
            logger.debug("Cache HIT: %s", key)
            return json.loads(value)
        logger.debug("Cache MISS: %s", key)
        return None
    except (redis.RedisError, json.JSONDecodeError) as e:
        logger.warning("Cache get error for key %s: %s", key, e)
        return None


def set_cache(key: str, value: Any, ttl: int = 300):
    """
    Guarda un valor en el cache con TTL en segundos.

    Args:
        key: Clave del cache
        value: Valor a guardar (se serializa a JSON)
        ttl: Tiempo de vida en segundos (default: 300 = 5 min)
    """
    client = get_redis_client()
    if not client:
        return

    try:
        serialized = json.dumps(value, default=str)
        client.set(name=key, value=serialized, ex=ttl)
        logger.debug("Cache SET: %s (TTL: %ds)", key, ttl)
    except (redis.RedisError, TypeError) as e:
        logger.warning("Cache set error for key %s: %s", key, e)


def delete_cache_pattern(pattern: str) -> int:
    """
    Elimina todas las keys que coincidan con el patron.

    Args:
        pattern: Patron Redis (ej: "products:*")

    Returns:
        int: Numero de keys eliminadas.
    """
    client = get_redis_client()
    if not client:
        return 0

    try:
        keys = client.keys(pattern)
        if keys:
            deleted = client.delete(*keys)
            logger.debug("Cache INVALIDATE: pattern=%s, deleted=%d", pattern, deleted)
            return deleted
        return 0
    except redis.RedisError as e:
        logger.warning("Cache delete error for pattern %s: %s", pattern, e)
        return 0


def build_cache_key(prefix: str, **kwargs) -> str:
    """
    Construye una key de cache con prefijo y parametros.

    Los parametros se ordenan alfabeticamente y se hashean
    para crear una key unica y deterministica.

    Args:
        prefix: Prefijo de la key (ej: "products")
        **kwargs: Parametros para construir la key

    Returns:
        str: Key de cache (ej: "products:list:page=1:per_page=10:abc123")

    Ejemplo:
        build_cache_key("products", page=1, per_page=10, category_id=1)
        # -> "products:list:page=1:per_page=10:category_id=1"
    """
    if not kwargs:
        return prefix

    # Ordenar parametros para keys consistentes
    sorted_params = sorted(kwargs.items())
    param_string = ":".join(f"{k}={v}" for k, v in sorted_params if v is not None)

    if not param_string:
        return prefix

    # Hashear parametros largos para evitar keys demasiado largas
    if len(param_string) > 100:
        param_hash = hashlib.md5(param_string.encode()).hexdigest()[:12]
        return f"{prefix}:{param_hash}"

    return f"{prefix}:{param_string}"


def cache_response(ttl: int = 300, prefix: str = ""):
    """
    Decorator para cachear la respuesta de un endpoint GET.

    Args:
        ttl: Tiempo de vida en segundos (default: 300 = 5 min)
        prefix: Prefijo para las keys de cache

    Uso:
        @router.get("/", response_model=ProductList)
        @cache_response(ttl=180, prefix="products")
        def list_products(page: int = 1, per_page: int = 10, ...):
            ...

    El decorator:
        1. Construye una key con el prefijo + parametros de la funcion
        2. Busca en Redis (cache hit → retorna valor cacheado)
        3. Si no hay cache, ejecuta la funcion
        4. Guarda el resultado en Redis con el TTL especificado
        5. Retorna el resultado
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Construir key de cache
            # Excluir db y current_user de los parametros de cache
            cache_params = {
                k: v for k, v in kwargs.items()
                if k not in ("db", "current_user") and v is not None
            }
            cache_key = build_cache_key(prefix, **cache_params)

            # Intentar obtener del cache
            cached = get_cache(cache_key)
            if cached is not None:
                return cached

            # Ejecutar la funcion original
            result = func(*args, **kwargs)

            # Guardar en cache si es exitoso
            if result is not None:
                # Convertir Pydantic model a dict si es necesario
                if hasattr(result, "model_dump"):
                    cache_value = result.model_dump()
                elif hasattr(result, "dict"):
                    cache_value = result.dict()
                else:
                    cache_value = result

                set_cache(cache_key, cache_value, ttl)

            return result
        return wrapper
    return decorator
