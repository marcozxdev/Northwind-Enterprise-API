# tests/test_customers.py
#
# Tests para los endpoints de Customers (Clientes).
#
# Archivos de endpoints que se testean: routers/customers.py
# Esquemas que se validan: schemas/customers.py
#
# Tests:
#
#   test_listar_clientes():
#     - GET /api/customers retorna 200 y una lista paginada.
#
#   test_obtener_cliente_por_id():
#     - GET /api/customers/{id} retorna 200 si existe.
#     - GET /api/customers/{id} retorna 404 si no existe.
#
#   test_crear_cliente():
#     - POST /api/customers con datos validos retorna 201.
#
#   test_crear_cliente_duplicado():
#     - POST /api/customers con customer_id existente retorna 400.
#
#   test_actualizar_cliente():
#     - PUT /api/customers/{id} retorna 200 si existe.
#
#   test_eliminar_cliente():
#     - DELETE /api/customers/{id} retorna 204 si existe.
#
#   test_filtrar_por_pais():
#     - GET /api/customers?country=Germany retorna clientes de Alemania.
#
#   test_permisos_viewer():
#     - Viewer puede hacer GET pero no POST/PUT/DELETE.
#
#   test_permisos_user():
#     - User puede hacer GET/POST/PUT pero no DELETE.


from fastapi.testclient import TestClient

# ============================================================================
# TESTS DE LISTAR CLIENTES
# ============================================================================


class TestListCustomers:
    """Tests para GET /api/customers."""

    def test_listar_clientes(self, client: TestClient, admin_headers: dict):
        """Listar clientes retorna 200 con estructura paginada."""
        response = client.get(
            "/northwind/api/customers",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert isinstance(data["items"], list)
        assert data["total"] > 0

    def test_listar_clientes_paginacion(self, client: TestClient, admin_headers: dict):
        """Listar clientes con paginacion personalizada."""
        response = client.get(
            "/northwind/api/customers?page=1&per_page=5",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert len(data["items"]) <= 5
        assert data["per_page"] == 5


# ============================================================================
# TESTS DE OBTENER CLIENTE POR ID
# ============================================================================


class TestGetCustomer:
    """Tests para GET /api/customers/{customer_id}."""

    def test_obtener_cliente_existente(self, client: TestClient, admin_headers: dict):
        """Obtener cliente existente retorna 200."""
        response = client.get(
            "/northwind/api/customers/ALFKI",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["customer_id"] == "ALFKI"
        assert data["company_name"] == "Alfreds Futterkiste"

    def test_obtener_cliente_no_existe(self, client: TestClient, admin_headers: dict):
        """Obtener cliente inexistente retorna 404."""
        response = client.get(
            "/northwind/api/customers/XXXXX",
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE CREAR CLIENTE
# ============================================================================


class TestCreateCustomer:
    """Tests para POST /api/customers."""

    def test_crear_cliente(self, client: TestClient, admin_headers: dict):
        """Crear cliente con datos validos retorna 201."""
        new_customer = {
            "customer_id": "NEW01",
            "company_name": "New Test Company",
            "contact_name": "Test Contact",
            "contact_title": "Owner",
            "address": "123 Test Ave",
            "city": "TestCity",
            "country": "TestCountry",
            "phone": "555-0100",
        }

        response = client.post(
            "/northwind/api/customers",
            json=new_customer,
            headers=admin_headers,
        )
        assert response.status_code == 201

        data = response.json()
        assert data["customer_id"] == "NEW01"
        assert data["company_name"] == "New Test Company"

    def test_crear_cliente_duplicado(self, client: TestClient, admin_headers: dict):
        """Crear cliente con customer_id existente retorna 400."""
        duplicate_customer = {
            "customer_id": "ALFKI",  # Ya existe
            "company_name": "Duplicate Company",
        }

        response = client.post(
            "/northwind/api/customers",
            json=duplicate_customer,
            headers=admin_headers,
        )
        assert response.status_code == 400

    def test_crear_cliente_campos_requeridos(self, client: TestClient, admin_headers: dict):
        """Crear cliente sin campos requeridos retorna 422."""
        incomplete_customer = {
            "contact_name": "Missing fields",
        }

        response = client.post(
            "/northwind/api/customers",
            json=incomplete_customer,
            headers=admin_headers,
        )
        assert response.status_code == 422


# ============================================================================
# TESTS DE ACTUALIZAR CLIENTE
# ============================================================================


class TestUpdateCustomer:
    """Tests para PUT /api/customers/{customer_id}."""

    def test_actualizar_cliente(self, client: TestClient, admin_headers: dict):
        """Actualizar cliente existente retorna 200."""
        update_data = {
            "company_name": "Updated Company Name",
            "contact_name": "Updated Contact",
        }

        response = client.put(
            "/northwind/api/customers/ALFKI",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["company_name"] == "Updated Company Name"

    def test_actualizar_cliente_no_existe(self, client: TestClient, admin_headers: dict):
        """Actualizar cliente inexistente retorna 404."""
        update_data = {"company_name": "Updated"}

        response = client.put(
            "/northwind/api/customers/XXXXX",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE ELIMINAR CLIENTE
# ============================================================================


class TestDeleteCustomer:
    """Tests para DELETE /api/customers/{customer_id}."""

    def test_eliminar_cliente(self, client: TestClient, admin_headers: dict):
        """Eliminar cliente existente retorna 204."""
        # Primero crear uno nuevo para eliminar
        new_customer = {
            "customer_id": "DEL01",
            "company_name": "To Delete",
        }
        client.post(
            "/northwind/api/customers",
            json=new_customer,
            headers=admin_headers,
        )

        response = client.delete(
            "/northwind/api/customers/DEL01",
            headers=admin_headers,
        )
        assert response.status_code == 204

    def test_eliminar_cliente_no_existe(self, client: TestClient, admin_headers: dict):
        """Eliminar cliente inexistente retorna 404."""
        response = client.delete(
            "/northwind/api/customers/XXXXX",
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE FILTROS
# ============================================================================


class TestFilterCustomers:
    """Tests para filtros de clientes."""

    def test_filtrar_por_pais(self, client: TestClient, admin_headers: dict):
        """Filtrar clientes por pais retorna solo los de ese pais."""
        response = client.get(
            "/northwind/api/customers?country=Germany",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for customer in data["items"]:
            assert customer["country"] == "Germany"

    def test_filtrar_por_ciudad(self, client: TestClient, admin_headers: dict):
        """Filtrar clientes por ciudad retorna solo los de esa ciudad."""
        response = client.get(
            "/northwind/api/customers?city=London",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for customer in data["items"]:
            assert customer["city"] == "London"

    def test_filtrar_por_empresa(self, client: TestClient, admin_headers: dict):
        """Filtrar clientes por nombre de empresa (busqueda parcial)."""
        response = client.get(
            "/northwind/api/customers?company_name=Alfreds",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["total"] >= 1


# ============================================================================
# TESTS DE PERMISOS
# ============================================================================


class TestCustomerPermissions:
    """Tests de permisos por rol para clientes."""

    def test_viewer_puede_leer(self, client: TestClient, viewer_headers: dict):
        """Viewer puede listar clientes (GET)."""
        response = client.get(
            "/northwind/api/customers",
            headers=viewer_headers,
        )
        assert response.status_code == 200

    def test_viewer_no_puede_crear(self, client: TestClient, viewer_headers: dict):
        """Viewer no puede crear clientes (POST)."""
        new_customer = {
            "customer_id": "FAIL",
            "company_name": "Should Fail",
        }
        response = client.post(
            "/northwind/api/customers",
            json=new_customer,
            headers=viewer_headers,
        )
        assert response.status_code == 403

    def test_user_puede_crear(self, client: TestClient, user_headers: dict):
        """User puede crear clientes (POST)."""
        new_customer = {
            "customer_id": "USR01",
            "company_name": "User Created",
        }
        response = client.post(
            "/northwind/api/customers",
            json=new_customer,
            headers=user_headers,
        )
        assert response.status_code == 201

    def test_user_no_puede_eliminar(self, client: TestClient, user_headers: dict):
        """User no puede eliminar clientes (DELETE)."""
        response = client.delete(
            "/northwind/api/customers/ALFKI",
            headers=user_headers,
        )
        assert response.status_code == 403

    def test_sin_auth_acceso_denegado(self, client: TestClient):
        """Sin token de autenticacion retorna 401."""
        response = client.get("/northwind/api/customers")
        assert response.status_code == 401
