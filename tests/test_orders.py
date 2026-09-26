# tests/test_orders.py
#
# Tests para los endpoints de Orders (Ordenes).
#
# Archivos de endpoints que se testean: routers/orders.py
# Esquemas que se validan: schemas/orders.py
#
# Tests:
#
#   test_listar_ordenes():
#     - GET /api/orders retorna 200 y una lista paginada.
#
#   test_obtener_orden_por_id():
#     - GET /api/orders/{id} retorna 200 si existe.
#     - GET /api/orders/{id} retorna 404 si no existe.
#
#   test_crear_orden_con_detalles():
#     - POST /api/orders con detalles retorna 201.
#
#   test_actualizar_orden():
#     - PUT /api/orders/{id} retorna 200 si existe.
#
#   test_eliminar_orden():
#     - DELETE /api/orders/{id} retorna 204 si existe.
#
#   test_filtrar_por_cliente():
#     - GET /api/orders?customer_id=ALFKI retorna ordenes de ese cliente.
#
#   test_filtrar_por_fecha():
#     - GET /api/orders?date_from=1996-07-01&date_to=1996-07-31
#
#   test_orden_incluye_detalles():
#     - GET /api/orders/{id} incluye details con products.
#


import pytest
from fastapi.testclient import TestClient


# ============================================================================
# TESTS DE LISTAR ORDENES
# ============================================================================


class TestListOrders:
    """Tests para GET /api/orders."""

    def test_listar_ordenes(self, client: TestClient, admin_headers: dict):
        """Listar ordenes retorna 200 con estructura paginada."""
        response = client.get(
            "/northwind/api/orders",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] > 0

    def test_listar_ordenes_con_relaciones(self, client: TestClient, admin_headers: dict):
        """Ordenes deben incluir customer_name, employee_name, shipper_name."""
        response = client.get(
            "/northwind/api/orders?per_page=1",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        if len(data["items"]) > 0:
            order = data["items"][0]
            assert "customer_name" in order
            assert "employee_name" in order
            assert "shipper_name" in order


# ============================================================================
# TESTS DE OBTENER ORDEN POR ID
# ============================================================================


class TestGetOrder:
    """Tests para GET /api/orders/{order_id}."""

    def test_obtener_orden_existente(self, client: TestClient, admin_headers: dict):
        """Obtener orden existente retorna 200 con detalles."""
        response = client.get(
            "/northwind/api/orders/10248",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["order_id"] == 10248
        assert "details" in data
        assert isinstance(data["details"], list)

    def test_obtener_orden_no_existe(self, client: TestClient, admin_headers: dict):
        """Obtener orden inexistente retorna 404."""
        response = client.get(
            "/northwind/api/orders/99999",
            headers=admin_headers,
        )
        assert response.status_code == 404

    def test_orden_incluye_detalles(self, client: TestClient, admin_headers: dict):
        """La respuesta de una orden incluye order_details."""
        response = client.get(
            "/northwind/api/orders/10248",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert len(data["details"]) > 0

        detail = data["details"][0]
        assert "product_id" in detail
        assert "unit_price" in detail
        assert "quantity" in detail
        assert "subtotal" in detail


# ============================================================================
# TESTS DE CREAR ORDEN
# ============================================================================


class TestCreateOrder:
    """Tests para POST /api/orders."""

    def test_crear_orden_con_detalles(self, client: TestClient, admin_headers: dict):
        """Crear orden con detalles retorna 201."""
        new_order = {
            "customer_id": "ALFKI",
            "employee_id": 1,
            "ship_via": 1,
            "freight": 10.50,
            "ship_name": "Test Order",
            "ship_address": "123 Ship St",
            "ship_city": "TestCity",
            "ship_country": "TestCountry",
            "details": [
                {
                    "product_id": 1,
                    "unit_price": 18.00,
                    "quantity": 10,
                    "discount": 0,
                }
            ],
        }

        response = client.post(
            "/northwind/api/orders",
            json=new_order,
            headers=admin_headers,
        )
        assert response.status_code == 201

        data = response.json()
        assert data["customer_id"] == "ALFKI"
        assert len(data["details"]) == 1

    def test_crear_orden_sin_detalles(self, client: TestClient, admin_headers: dict):
        """Crear orden sin detalles retorna 201."""
        new_order = {
            "customer_id": "ALFKI",
            "employee_id": 1,
        }

        response = client.post(
            "/northwind/api/orders",
            json=new_order,
            headers=admin_headers,
        )
        assert response.status_code == 201


# ============================================================================
# TESTS DE ACTUALIZAR ORDEN
# ============================================================================


class TestUpdateOrder:
    """Tests para PUT /api/orders/{order_id}."""

    def test_actualizar_orden(self, client: TestClient, admin_headers: dict):
        """Actualizar orden existente retorna 200."""
        update_data = {
            "freight": 99.99,
            "ship_name": "Updated Order",
        }

        response = client.put(
            "/northwind/api/orders/10248",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["freight"] == 99.99

    def test_actualizar_orden_no_existe(self, client: TestClient, admin_headers: dict):
        """Actualizar orden inexistente retorna 404."""
        response = client.put(
            "/northwind/api/orders/99999",
            json={"freight": 10.00},
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE ELIMINAR ORDEN
# ============================================================================


class TestDeleteOrder:
    """Tests para DELETE /api/orders/{order_id}."""

    def test_eliminar_orden(self, client: TestClient, admin_headers: dict):
        """Eliminar orden existente retorna 204."""
        # Crear orden para eliminar
        new_order = {
            "customer_id": "ALFKI",
            "details": [
                {
                    "product_id": 1,
                    "unit_price": 18.00,
                    "quantity": 5,
                    "discount": 0,
                }
            ],
        }
        create_resp = client.post(
            "/northwind/api/orders",
            json=new_order,
            headers=admin_headers,
        )
        order_id = create_resp.json()["order_id"]

        response = client.delete(
            f"/northwind/api/orders/{order_id}",
            headers=admin_headers,
        )
        assert response.status_code == 204

    def test_eliminar_orden_no_existe(self, client: TestClient, admin_headers: dict):
        """Eliminar orden inexistente retorna 404."""
        response = client.delete(
            "/northwind/api/orders/99999",
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE FILTROS
# ============================================================================


class TestFilterOrders:
    """Tests para filtros de ordenes."""

    def test_filtrar_por_cliente(self, client: TestClient, admin_headers: dict):
        """Filtrar ordenes por cliente retorna solo las de ese cliente."""
        response = client.get(
            "/northwind/api/orders?customer_id=ALFKI",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for order in data["items"]:
            assert order["customer_id"] == "ALFKI"

    def test_filtrar_por_empleado(self, client: TestClient, admin_headers: dict):
        """Filtrar ordenes por empleado."""
        response = client.get(
            "/northwind/api/orders?employee_id=1",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for order in data["items"]:
            assert order["employee_id"] == 1

    def test_filtrar_por_estado_envio(self, client: TestClient, admin_headers: dict):
        """Filtrar ordenes enviadas (shipped_date not null)."""
        response = client.get(
            "/northwind/api/orders?shipped=true",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        for order in data["items"]:
            assert order["shipped_date"] is not None


# ============================================================================
# TESTS DE PERMISOS
# ============================================================================


class TestOrderPermissions:
    """Tests de permisos por rol para ordenes."""

    def test_viewer_puede_leer(self, client: TestClient, viewer_headers: dict):
        """Viewer puede listar ordenes (GET)."""
        response = client.get(
            "/northwind/api/orders",
            headers=viewer_headers,
        )
        assert response.status_code == 200

    def test_viewer_no_puede_crear(self, client: TestClient, viewer_headers: dict):
        """Viewer no puede crear ordenes (POST)."""
        new_order = {
            "customer_id": "ALFKI",
            "details": [{"product_id": 1, "unit_price": 10, "quantity": 1, "discount": 0}],
        }
        response = client.post(
            "/northwind/api/orders",
            json=new_order,
            headers=viewer_headers,
        )
        assert response.status_code == 403

    def test_user_puede_crear(self, client: TestClient, user_headers: dict):
        """User puede crear ordenes (POST)."""
        new_order = {
            "customer_id": "ALFKI",
            "details": [{"product_id": 1, "unit_price": 10, "quantity": 1, "discount": 0}],
        }
        response = client.post(
            "/northwind/api/orders",
            json=new_order,
            headers=user_headers,
        )
        assert response.status_code == 201

    def test_user_no_puede_eliminar(self, client: TestClient, user_headers: dict):
        """User no puede eliminar ordenes (DELETE)."""
        response = client.delete(
            "/northwind/api/orders/10248",
            headers=user_headers,
        )
        assert response.status_code == 403
