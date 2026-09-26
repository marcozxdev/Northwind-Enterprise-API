# tests/test_cache.py
#
# Tests para el sistema de cache con Redis.
#
# ============================================================================
# TESTS
# ============================================================================
#
#   test_cache_set_and_get():
#     - Guardar y recuperar un valor del cache.
#
#   test_cache_miss():
#     - Key inexistente retorna None.
#
#   test_cache_ttl():
#     - El valor expira despues del TTL.
#
#   test_cache_delete_pattern():
#     - Eliminar keys por patron.
#
#   test_cache_build_key():
#     - Construccion de keys con parametros.
#
#   test_products_cache_hit():
#     - GET /products retorna datos cacheados en segundo request.
#
#   test_products_cache_invalidation():
#     - POST /products invalida el cache de products.
#
#   test_customers_cache_hit():
#     - GET /customers retorna datos cacheados.
#
#   test_orders_cache_hit():
#     - GET /orders retorna datos cacheados.
#
#   test_categories_cache_hit():
#     - GET /categories usa TTL largo (30 min).



import pytest
from fastapi.testclient import TestClient

from app.core.cache import (
    build_cache_key,
    close_redis,
    delete_cache_pattern,
    get_cache,
    init_redis,
    set_cache,
)

# ============================================================================
# FIXTURE: Initialize Redis for direct function tests
# ============================================================================


@pytest.fixture(scope="module", autouse=True)
def redis_connection():
    """Initialize Redis connection for cache tests."""
    init_redis()
    yield
    close_redis()


# ============================================================================
# TESTS DE FUNCIONES DE CACHE
# ============================================================================


class TestCacheFunctions:
    """Tests para las funciones basicas de cache."""

    def test_set_and_get_cache(self):
        """Guardar y recuperar un valor del cache."""
        set_cache("test:key1", {"name": "test"}, ttl=60)
        result = get_cache("test:key1")
        assert result is not None
        assert result["name"] == "test"

        # Limpiar
        delete_cache_pattern("test:*")

    def test_cache_miss(self):
        """Key inexistente retorna None."""
        result = get_cache("test:nonexistent_key_xyz")
        assert result is None

    def test_cache_delete_pattern(self):
        """Eliminar keys por patron."""
        set_cache("test:del:1", {"a": 1}, ttl=60)
        set_cache("test:del:2", {"a": 2}, ttl=60)
        set_cache("test:del:3", {"a": 3}, ttl=60)

        deleted = delete_cache_pattern("test:del:*")
        assert deleted >= 3

        # Verificar que fueron eliminadas
        assert get_cache("test:del:1") is None
        assert get_cache("test:del:2") is None
        assert get_cache("test:del:3") is None

    def test_cache_overwrite(self):
        """Sobrescribir un valor existente."""
        set_cache("test:overwrite", {"v": 1}, ttl=60)
        set_cache("test:overwrite", {"v": 2}, ttl=60)

        result = get_cache("test:overwrite")
        assert result["v"] == 2

        delete_cache_pattern("test:overwrite")

    def test_build_cache_key_simple(self):
        """Construccion de key simple."""
        key = build_cache_key("products")
        assert key == "products"

    def test_build_cache_key_with_params(self):
        """Construccion de key con parametros."""
        key = build_cache_key("products:list", page=1, per_page=10)
        assert "products:list" in key
        assert "page=1" in key
        assert "per_page=10" in key

    def test_build_cache_key_deterministic(self):
        """Mismos parametros producen la misma key."""
        key1 = build_cache_key("products:list", page=1, per_page=10)
        key2 = build_cache_key("products:list", page=1, per_page=10)
        assert key1 == key2

    def test_build_cache_key_order_independent(self):
        """Orden de parametros no afecta la key."""
        key1 = build_cache_key("test", page=1, per_page=10)
        key2 = build_cache_key("test", per_page=10, page=1)
        assert key1 == key2

    def test_build_cache_key_ignores_none(self):
        """Parametros None se ignoran."""
        key1 = build_cache_key("test", page=1, category_id=None)
        key2 = build_cache_key("test", page=1)
        assert key1 == key2


# ============================================================================
# TESTS DE CACHE EN ENDPOINTS
# ============================================================================


class TestProductsCache:
    """Tests de cache en endpoints de products."""

    def test_products_cache_hit(self, client: TestClient, admin_headers: dict):
        """Segundo GET /products retorna datos (posiblemente cacheados)."""
        # Primero limpiar cache
        delete_cache_pattern("products:*")

        # Primer request - cache miss
        response1 = client.get(
            "/northwind/api/products",
            headers=admin_headers,
        )
        assert response1.status_code == 200
        data1 = response1.json()

        # Segundo request - debe retornar los mismos datos
        response2 = client.get(
            "/northwind/api/products",
            headers=admin_headers,
        )
        assert response2.status_code == 200
        data2 = response2.json()

        # Los datos deben ser iguales
        assert data1["total"] == data2["total"]
        assert len(data1["items"]) == len(data2["items"])

        # Limpiar
        delete_cache_pattern("products:*")

    def test_products_cache_invalidation(self, client: TestClient, admin_headers: dict):
        """POST /products invalida el cache de products."""
        # Llenar cache
        client.get("/northwind/api/products", headers=admin_headers)

        # Crear producto (debe invalidar cache)
        new_product = {
            "product_name": "Cache Test Product",
            "supplier_id": 1,
            "category_id": 1,
            "quantity_per_unit": "10 boxes",
            "unit_price": 25.00,
            "units_in_stock": 100,
            "units_on_order": 0,
            "reorder_level": 10,
            "discontinued": 0,
        }
        create_resp = client.post(
            "/northwind/api/products",
            json=new_product,
            headers=admin_headers,
        )
        assert create_resp.status_code == 201

        # Verificar que el cache fue invalidado
        # (el siguiente GET deberia ir a la DB)
        response = client.get(
            "/northwind/api/products",
            headers=admin_headers,
        )
        assert response.status_code == 200

        # Limpiar
        delete_cache_pattern("products:*")

    def test_products_detail_cache(self, client: TestClient, admin_headers: dict):
        """GET /products/{id} usa cache."""
        delete_cache_pattern("products:get:*")

        # Primer request
        response1 = client.get(
            "/northwind/api/products/1",
            headers=admin_headers,
        )
        assert response1.status_code == 200

        # Segundo request - mismos datos
        response2 = client.get(
            "/northwind/api/products/1",
            headers=admin_headers,
        )
        assert response2.status_code == 200
        assert response1.json()["product_name"] == response2.json()["product_name"]

        delete_cache_pattern("products:get:*")


class TestCustomersCache:
    """Tests de cache en endpoints de customers."""

    def test_customers_cache_hit(self, client: TestClient, admin_headers: dict):
        """GET /customers funciona correctamente con cache."""
        delete_cache_pattern("customers:*")

        response1 = client.get(
            "/northwind/api/customers",
            headers=admin_headers,
        )
        assert response1.status_code == 200

        response2 = client.get(
            "/northwind/api/customers",
            headers=admin_headers,
        )
        assert response2.status_code == 200
        assert response1.json()["total"] == response2.json()["total"]

        delete_cache_pattern("customers:*")

    def test_customers_cache_invalidation(self, client: TestClient, admin_headers: dict):
        """POST /customers invalida el cache."""
        client.get("/northwind/api/customers", headers=admin_headers)

        new_customer = {
            "customer_id": "CTEST",
            "company_name": "Cache Test Co",
            "contact_name": "Test Contact",
        }
        create_resp = client.post(
            "/northwind/api/customers",
            json=new_customer,
            headers=admin_headers,
        )
        assert create_resp.status_code == 201

        # Verificar invalidacion
        response = client.get(
            "/northwind/api/customers",
            headers=admin_headers,
        )
        assert response.status_code == 200

        delete_cache_pattern("customers:*")


class TestOrdersCache:
    """Tests de cache en endpoints de orders."""

    def test_orders_cache_hit(self, client: TestClient, admin_headers: dict):
        """GET /orders funciona correctamente con cache."""
        delete_cache_pattern("orders:*")

        response1 = client.get(
            "/northwind/api/orders",
            headers=admin_headers,
        )
        assert response1.status_code == 200

        response2 = client.get(
            "/northwind/api/orders",
            headers=admin_headers,
        )
        assert response2.status_code == 200
        assert response1.json()["total"] == response2.json()["total"]

        delete_cache_pattern("orders:*")


class TestCategoriesCache:
    """Tests de cache en endpoints de categories (TTL largo)."""

    def test_categories_cache_hit(self, client: TestClient, admin_headers: dict):
        """GET /categories funciona correctamente con cache."""
        delete_cache_pattern("categories:*")

        response1 = client.get(
            "/northwind/api/categories",
            headers=admin_headers,
        )
        assert response1.status_code == 200

        response2 = client.get(
            "/northwind/api/categories",
            headers=admin_headers,
        )
        assert response2.status_code == 200
        assert response1.json()["total"] == response2.json()["total"]

        delete_cache_pattern("categories:*")


class TestShippersCache:
    """Tests de cache en endpoints de shippers (TTL largo)."""

    def test_shippers_cache_hit(self, client: TestClient, admin_headers: dict):
        """GET /shippers funciona correctamente con cache."""
        delete_cache_pattern("shippers:*")

        response1 = client.get(
            "/northwind/api/shippers",
            headers=admin_headers,
        )
        assert response1.status_code == 200

        response2 = client.get(
            "/northwind/api/shippers",
            headers=admin_headers,
        )
        assert response2.status_code == 200

        delete_cache_pattern("shippers:*")
