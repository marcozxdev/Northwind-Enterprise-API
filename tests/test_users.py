# tests/test_users.py
#
# Tests para los endpoints de Users (Gestion de usuarios).
#
# Archivos de endpoints que se testean: routers/users.py
# Esquemas que se validan: schemas/users.py
#
# Tests:
#
#   test_listar_usuarios():
#     - GET /api/users retorna 200 (solo admin).
#
#   test_obtener_usuario():
#     - GET /api/users/{id} retorna 200 si existe.
#
#   test_actualizar_usuario():
#     - PUT /api/users/{id} retorna 200.
#
#   test_desactivar_usuario():
#     - DELETE /api/users/{id} retorna 204.
#
#   test_asignar_roles():
#     - PUT /api/users/{id}/roles retorna 200.
#
#   test_no_admin_no_accede():
#     - User/Viewer no pueden listar usuarios (403).
#
#   test_no_puede_desactivarse_a_si_mismo():
#     - Admin no puede desactivar su propia cuenta.
#


from fastapi.testclient import TestClient

# ============================================================================
# TESTS DE LISTAR USUARIOS
# ============================================================================


class TestListUsers:
    """Tests para GET /api/users."""

    def test_listar_usuarios_admin(self, client: TestClient, admin_headers: dict):
        """Admin puede listar todos los usuarios."""
        response = client.get(
            "/northwind/api/users",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 5  # Tenemos 5 usuarios en el seed

    def test_user_no_puede_listar(self, client: TestClient, user_headers: dict):
        """User no puede listar usuarios (403)."""
        response = client.get(
            "/northwind/api/users",
            headers=user_headers,
        )
        assert response.status_code == 403

    def test_viewer_no_puede_listar(self, client: TestClient, viewer_headers: dict):
        """Viewer no puede listar usuarios (403)."""
        response = client.get(
            "/northwind/api/users",
            headers=viewer_headers,
        )
        assert response.status_code == 403


# ============================================================================
# TESTS DE OBTENER USUARIO POR ID
# ============================================================================


class TestGetUser:
    """Tests para GET /api/users/{user_id}."""

    def test_obtener_usuario_existente(self, client: TestClient, admin_headers: dict):
        """Admin puede obtener cualquier usuario por ID."""
        response = client.get(
            "/northwind/api/users/1",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["user_id"] == 1
        assert data["username"] == "admin"
        assert "roles" in data

    def test_obtener_usuario_no_existe(self, client: TestClient, admin_headers: dict):
        """Obtener usuario inexistente retorna 404."""
        response = client.get(
            "/northwind/api/users/999",
            headers=admin_headers,
        )
        assert response.status_code == 404


# ============================================================================
# TESTS DE ACTUALIZAR USUARIO
# ============================================================================


class TestUpdateUser:
    """Tests para PUT /api/users/{user_id}."""

    def test_actualizar_usuario(self, client: TestClient, admin_headers: dict):
        """Admin puede actualizar cualquier usuario."""
        update_data = {
            "full_name": "Updated Name",
        }

        response = client.put(
            "/northwind/api/users/3",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["full_name"] == "Updated Name"

    def test_actualizar_usuario_email_duplicado(self, client: TestClient, admin_headers: dict):
        """Actualizar con email existente retorna 400."""
        update_data = {
            "email": "admin@northwind.com",  # Ya usado por admin
        }

        response = client.put(
            "/northwind/api/users/3",
            json=update_data,
            headers=admin_headers,
        )
        assert response.status_code == 400

    def test_user_no_puede_modificar_otros(self, client: TestClient, user_headers: dict):
        """User no puede modificar otros usuarios (solo admin)."""
        update_data = {"full_name": "Should Fail"}

        response = client.put(
            "/northwind/api/users/1",
            json=update_data,
            headers=user_headers,
        )
        assert response.status_code == 403


# ============================================================================
# TESTS DE DESACTIVAR USUARIO
# ============================================================================


class TestDeactivateUser:
    """Tests para DELETE /api/users/{user_id} (soft delete)."""

    def test_desactivar_usuario(self, client: TestClient, admin_headers: dict):
        """Admin puede desactivar usuarios."""
        # Crear usuario para desactivar
        new_user = {
            "username": "to_deactivate",
            "email": "deactivate@test.com",
            "password": "TestPass123!",
        }
        create_resp = client.post(
            "/northwind/api/auth/register",
            json=new_user,
        )
        user_id = create_resp.json()["user_id"]

        response = client.delete(
            f"/northwind/api/users/{user_id}",
            headers=admin_headers,
        )
        assert response.status_code == 204

    def test_no_puede_desactivarse_a_si_mismo(self, client: TestClient, admin_headers: dict):
        """Admin no puede desactivar su propia cuenta."""
        response = client.delete(
            "/northwind/api/users/1",  # admin user_id = 1
            headers=admin_headers,
        )
        assert response.status_code == 400

    def test_user_no_puede_desactivar(self, client: TestClient, user_headers: dict):
        """User no puede desactivar usuarios (403)."""
        response = client.delete(
            "/northwind/api/users/4",
            headers=user_headers,
        )
        assert response.status_code == 403


# ============================================================================
# TESTS DE ASIGNAR ROLES
# ============================================================================


class TestAssignRoles:
    """Tests para PUT /api/users/{user_id}/roles."""

    def test_asignar_roles(self, client: TestClient, admin_headers: dict):
        """Admin puede asignar roles a usuarios."""
        # Primero obtener los roles disponibles
        response = client.get(
            "/northwind/api/users/3",
            headers=admin_headers,
        )
        assert response.status_code == 200

        # Asignar rol viewer (role_id=3) al usuario 3
        update_roles = {"role_ids": [2, 3]}  # user + viewer

        response = client.put(
            "/northwind/api/users/3/roles",
            json=update_roles,
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        role_names = [r["role_name"] for r in data["roles"]]
        assert "user" in role_names
        assert "viewer" in role_names

    def test_user_no_puede_asignar_roles(self, client: TestClient, user_headers: dict):
        """User no puede asignar roles (403)."""
        response = client.put(
            "/northwind/api/users/4/roles",
            json={"role_ids": [1]},
            headers=user_headers,
        )
        assert response.status_code == 403


# ============================================================================
# TESTS DE USUARIO INACTIVO
# ============================================================================


class TestInactiveUser:
    """Tests para usuario inactivo."""

    def test_usuario_inactivo_no_puede_login(self, client: TestClient):
        """Usuario inactivo no puede iniciar sesion."""
        response = client.post(
            "/northwind/api/auth/login",
            json={"username": "inactive", "password": "Viewer2024!"},
        )
        assert response.status_code == 403

    def test_usuario_inactivo_acceso_denegado(self, client: TestClient):
        """Token de usuario inactivo retorna 403 en endpoints protegidos."""
        from app.core.security import create_access_token

        # Crear token para usuario inactivo (user_id=6)
        token = create_access_token({"sub": "6", "roles": ["viewer"]})
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(
            "/northwind/api/auth/me",
            headers=headers,
        )
        assert response.status_code == 403
