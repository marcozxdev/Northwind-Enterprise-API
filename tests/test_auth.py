# tests/test_auth.py
#
# Tests para los endpoints de Autenticacion (auth).
#
# Archivos de endpoints que se testean: routers/auth.py
# Esquemas que se validan: schemas/users.py
#
# Tests:
#
#   test_login_exitoso():
#     - POST /api/auth/login con credenciales validas retorna 200.
#     - La respuesta contiene access_token y user.
#
#   test_login_credenciales_invalidas():
#     - POST /api/auth/login con password incorrecto retorna 401.
#     - POST /api/auth/login con usuario inexistente retorna 401.
#
#   test_register_exitoso():
#     - POST /api/auth/register con datos validos retorna 201.
#     - El usuario creado tiene el rol "viewer" por defecto.
#
#   test_register_usuario_duplicado():
#     - POST /api/auth/register con username existente retorna 400.
#     - POST /api/auth/register con email existente retorna 400.
#
#   test_obtener_perfil_autenticado():
#     - GET /api/auth/me con token valido retorna 200.
#     - GET /api/auth/me sin token retorna 401.
#
#   test_acceso_token_invalido():
#     - GET /api/auth/me con token invalido retorna 401.
#


import pytest
from fastapi.testclient import TestClient


# ============================================================================
# TESTS DE LOGIN
# ============================================================================


class TestLogin:
    """Tests para el endpoint POST /api/auth/login."""

    def test_login_exitoso(self, client: TestClient):
        """Login con credenciales validas retorna token JWT."""
        response = client.post(
            "/northwind/api/auth/login",
            json={"username": "admin", "password": "Northwind2024!"},
        )
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "admin"

    def test_login_password_incorrecto(self, client: TestClient):
        """Login con password incorrecto retorna 401."""
        response = client.post(
            "/northwind/api/auth/login",
            json={"username": "admin", "password": "wrong_password"},
        )
        assert response.status_code == 401

    def test_login_usuario_inexistente(self, client: TestClient):
        """Login con usuario que no existe retorna 401."""
        response = client.post(
            "/northwind/api/auth/login",
            json={"username": "nonexistent", "password": "password123"},
        )
        assert response.status_code == 401

    def test_login_campo_faltante(self, client: TestClient):
        """Login sin campo username retorna 422 (validacion)."""
        response = client.post(
            "/northwind/api/auth/login",
            json={"password": "password123"},
        )
        assert response.status_code == 422

    def test_login_campo_vacio(self, client: TestClient):
        """Login con username vacio retorna 422."""
        response = client.post(
            "/northwind/api/auth/login",
            json={"username": "", "password": "password123"},
        )
        assert response.status_code == 422


# ============================================================================
# TESTS DE REGISTER
# ============================================================================


class TestRegister:
    """Tests para el endpoint POST /api/auth/register."""

    def test_register_exitoso(self, client: TestClient):
        """Registro con datos validos retorna 201 y usuario creado."""
        response = client.post(
            "/northwind/api/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "TestPass123!",
                "full_name": "New User",
            },
        )
        assert response.status_code == 201

        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@test.com"
        assert data["full_name"] == "New User"
        assert data["is_active"] is True
        assert "hashed_password" not in data  # No deveolver password

    def test_register_usuario_duplicado(self, client: TestClient):
        """Registro con username existente retorna 400."""
        response = client.post(
            "/northwind/api/auth/register",
            json={
                "username": "admin",
                "email": "unique@test.com",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 400

    def test_register_email_duplicado(self, client: TestClient):
        """Registro con email existente retorna 400."""
        response = client.post(
            "/northwind/api/auth/register",
            json={
                "username": "uniqueuser",
                "email": "admin@northwind.com",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 400

    def test_register_email_invalido(self, client: TestClient):
        """Registro con email invalido retorna 422."""
        response = client.post(
            "/northwind/api/auth/register",
            json={
                "username": "testuser",
                "email": "not_an_email",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 422

    def test_register_password_corta(self, client: TestClient):
        """Registro con password menor a 6 caracteres retorna 422."""
        response = client.post(
            "/northwind/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@test.com",
                "password": "12345",
            },
        )
        assert response.status_code == 422


# ============================================================================
# TESTS DE PROFILE (GET /me)
# ============================================================================


class TestProfile:
    """Tests para el endpoint GET /api/auth/me."""

    def test_obtener_perfil_autenticado(self, client: TestClient, admin_headers: dict):
        """Obtener perfil con token valido retorna 200."""
        response = client.get(
            "/northwind/api/auth/me",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["username"] == "admin"
        assert "roles" in data

    def test_obtener_perfil_sin_token(self, client: TestClient):
        """Obtener perfil sin token retorna 401."""
        response = client.get("/northwind/api/auth/me")
        assert response.status_code == 401

    def test_obtener_perfil_token_invalido(self, client: TestClient):
        """Obtener perfil con token invalido retorna 401."""
        response = client.get(
            "/northwind/api/auth/me",
            headers={"Authorization": "Bearer invalid_token_here"},
        )
        assert response.status_code == 401

    def test_perfil_muestra_roles(self, client: TestClient, admin_headers: dict):
        """El perfil del admin debe incluir el rol 'admin'."""
        response = client.get(
            "/northwind/api/auth/me",
            headers=admin_headers,
        )
        assert response.status_code == 200

        data = response.json()
        role_names = [r["role_name"] for r in data["roles"]]
        assert "admin" in role_names
