# tests/test_products.py
#
# Tests para los endpoints de Products (Productos).
#
# Archivos de endpoints que se testean: routers/products.py
# Esquemas que se validan: schemas/products.py
#
# Tests:
#
#   test_listar_productos():
#     - GET /api/products retorna 200 y una lista paginada.
#
#   test_obtener_producto_por_id():
#     - GET /api/products/{id} retorna 200 si existe.
#     - GET /api/products/{id} retorna 404 si no existe.
#
#   test_crear_producto():
#     - POST /api/products con datos validos retorna 201.
#
#   test_actualizar_producto():
#     - PUT /api/products/{id} retorna 200 si existe.
#
#   test_eliminar_producto():
#     - DELETE /api/products/{id} retorna 204 si existe.
#
#   test_filtrar_por_categoria():
#     - GET /api/products?category_id=1 retorna productos de esa categoria.
#
#   test_filtrar_por_precio():
#     - GET /api/products?price_min=10&price_max=50 retorna productos en rango.
#
#   test_filtrar_por_stock():
#     - GET /api/products?in_stock=true retorna solo productos con stock.
#


from fastapi.testclient import TestClient

# ============================================================================
# TESTS DE LISTAR PRODUCTOS
# ============================================================================


class TestListProducts:
    """Tests para GET /api/products."""

    def test_listar_productos(self, client: TestClient, admin_headers: dict):
        """Listar productos retorna 200 con estructura paginada."""
        response = client.get(
            "/northwind/api/products",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] > 0

    def test_listar_productos_con_categoria(self, client: TestClient, admin_headers: dict):
        """Productos deben incluir category_name y supplier_company."""
        response = client.get(
            "/northwind/api/products?per_page=1",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        if len(data["items"]) > 0:
            product = data["items"][0]
            assert "category_name" in product
            assert "supplier_company" in product


# ============================================================================
# TESTS DE OBTENER PRODUCTO POR ID
# ============================================================================


class TestGetProduct:
    """Tests para GET /api/products/{product_id}."""

    def test_obtener_producto_existente(self, client: TestClient, admin_headers: dict):
        """Obtener producto existente retorna 200."""
        response = client.get(
            "/northwind/api/products/1",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["product_id"] == 1
        assert "product_name" in data

    def test_obtener_producto_no_existe(self, client: TestClient, admin_headers: dict):
        """Obtener producto inexistente retorna 404."""
        response = client.get(
            "/northwind/api/products/99999",
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE CREAR PRODUCTO
# ============================================================================


class TestCreateProduct:
    """Tests para POST /api/products."""

    def test_crear_producto(self, client: TestClient, admin_headers: dict):
        """Crear producto con datos validos retorna 201."""
        new_product = {
            "product_name": "Test Product",
            "supplier_id": 1,
            "category_id": 1,
            "quantity_per_unit": "10 boxes",
            "unit_price": 25.00,
            "units_in_stock": 100,
            "units_on_order": 0,
            "reorder_level": 10,
            "discontinued": 0,
        }

        response = client.post(
            "/northwind/api/products",
            json=new_product,
            headers=admin_headers,
        )
        assert response.status_code == 201

        data = response.json()
        assert data["product_name"] == "Test Product"
        assert data["unit_price"] == 25.00

    def test_crear_producto_campos_requeridos(self, client: TestClient, admin_headers: dict):
        """Crear producto sin product_name retorna 422."""
        incomplete_product = {
            "unit_price": 10.00,
        }

        response = client.post(
            "/northwind/api/products",
            json=incomplete_product,
            headers=admin_headers,
        )
        assert response.status_code == 422


# ============================================================================
# TESTS DE ACTUALIZAR PRODUCTO
# ============================================================================


class TestUpdateProduct:
    """Tests para PUT /api/products/{product_id}."""

    def test_actualizar_producto(self, client: TestClient, admin_headers: dict):
        """Actualizar producto existente retorna 200."""
        update_data = {
            "product_name": "Updated Product",
            "unit_price": 35.00,
        }

        response = client.put(
            "/northwind/api/products/1",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["product_name"] == "Updated Product"

    def test_actualizar_producto_no_existe(self, client: TestClient, admin_headers: dict):
        """Actualizar producto inexistente retorna 404."""
        response = client.put(
            "/northwind/api/products/99999",
            json={"product_name": "Updated"},
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE ELIMINAR PRODUCTO
# ============================================================================


class TestDeleteProduct:
    """Tests para DELETE /api/products/{product_id}."""

    def test_eliminar_producto(self, client: TestClient, admin_headers: dict):
        """Eliminar producto existente retorna 204."""
        # Crear producto para eliminar
        new_product = {
            "product_name": "To Delete",
            "discontinued": 0,
        }
        create_resp = client.post(
            "/northwind/api/products",
            json=new_product,
            headers=admin_headers,
        )
        product_id = create_resp.json()["product_id"]

        response = client.delete(
            f"/northwind/api/products/{product_id}",
            headers=admin_headers,
        )
        assert response.status_code == 204

    def test_eliminar_producto_no_existe(self, client: TestClient, admin_headers: dict):
        """Eliminar producto inexistente retorna 404."""
        response = client.delete(
            "/northwind/api/products/99999",
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE FILTROS
# ============================================================================


class TestFilterProducts:
    """Tests para filtros de productos."""

    def test_filtrar_por_categoria(self, client: TestClient, admin_headers: dict):
        """Filtrar productos por categoria retorna solo los de esa categoria."""
        response = client.get(
            "/northwind/api/products?category_id=1",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for product in data["items"]:
            assert product["category_id"] == 1

    def test_filtrar_por_precio_minimo(self, client: TestClient, admin_headers: dict):
        """Filtrar productos por precio minimo."""
        response = client.get(
            "/northwind/api/products?price_min=50",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for product in data["items"]:
            if product["unit_price"] is not None:
                assert product["unit_price"] >= 50

    def test_filtrar_por_stock(self, client: TestClient, admin_headers: dict):
        """Filtrar solo productos con stock disponible."""
        response = client.get(
            "/northwind/api/products?in_stock=true",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for product in data["items"]:
            if product["units_in_stock"] is not None:
                assert product["units_in_stock"] > 0


# ============================================================================
# TESTS DE PERMISOS
# ============================================================================


class TestProductPermissions:
    """Tests de permisos por rol para productos."""

    def test_viewer_puede_leer(self, client: TestClient, viewer_headers: dict):
        """Viewer puede listar productos (GET)."""
        response = client.get(
            "/northwind/api/products",
            headers=viewer_headers,
        )
        assert response.status_code == 200

    def test_viewer_no_puede_crear(self, client: TestClient, viewer_headers: dict):
        """Viewer no puede crear productos (POST)."""
        new_product = {
            "product_name": "Should Fail",
            "discontinued": 0,
        }
        response = client.post(
            "/northwind/api/products",
            json=new_product,
            headers=viewer_headers,
        )
        assert response.status_code == 403

    def test_user_puede_crear(self, client: TestClient, user_headers: dict):
        """User puede crear productos (POST)."""
        new_product = {
            "product_name": "User Product",
            "discontinued": 0,
        }
        response = client.post(
            "/northwind/api/products",
            json=new_product,
            headers=user_headers,
        )
        assert response.status_code == 201

    def test_user_no_puede_eliminar(self, client: TestClient, user_headers: dict):
        """User no puede eliminar productos (DELETE)."""
        response = client.delete(
            "/northwind/api/products/1",
            headers=user_headers,
        )
        assert response.status_code == 403
