# tests/conftest.py
#
# Configuracion compartida de pytest (fixtures).
#
# Este archivo contiene los fixtures que se usan en todos los tests.
# Pytest los carga automaticamente antes de cada test que los necesite.
#
# Fixtures:
#
#   client():
#     - Crea un TestClient de FastAPI apuntando a la app.
#     - Se usa para hacer peticiones HTTP simuladas.
#
#   db_session():
#     - Crea una sesion de PostgreSQL para tests.
#     - Cada test empieza con la BD limpia (rollback automatico).
#
#   auth_headers():
#     - Headers de autenticacion con token JWT valido.
#     - Se usa para endpoints protegidos.
#
#   admin_headers():
#     - Headers con token de usuario admin.
#
#   user_headers():
#     - Headers con token de usuario normal (user role).
#
#   viewer_headers():
#     - Headers con token de usuario viewer.
#
import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Configurar variables de entorno para tests
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_USER", "northwind_user")
os.environ.setdefault("DB_PASSWORD", "northwind_password")
os.environ.setdefault("DB_NAME", "northwind")
os.environ.setdefault("JWT_SECRET_KEY", "YOUR-SECRET-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXP_MIN", "40")

from app.core.database import Base, get_db
from app.core.security import create_access_token
from app.main import app


# ============================================================================
# DATABASE FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def db_engine():
    """
    Crea el engine de SQLAlchemy apuntando a PostgreSQL en Docker.
    Se usa una sola vez por toda la sesion de tests.
    """
    db_user = os.getenv("DB_USER", "northwind_user")
    db_password = os.getenv("DB_PASSWORD", "northwind_password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "northwind")

    database_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(
        database_url,
        poolclass=StaticPool,
    )

    yield engine

    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Crea una sesion de BD para cada test.
    Hace rollback automatico al finalizar para no contaminar otros tests.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """
    Crea un TestClient de FastAPI con la dependencia de BD overrideada.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# ============================================================================
# AUTH FIXTURES
# ============================================================================


def get_auth_token(username: str, password: str) -> str:
    """
    Funcion auxiliar para obtener un token JWT haciendo login.
    """
    from app.core.security import verify_password
    from app.models.users import User

    # Buscar usuario en la BD
    # Nota: Para tests, generamos el token directamente
    # En produccion se usaria el endpoint /auth/login

    # Crear token con datos mock
    # En tests reales, deberiamos buscar el usuario en la BD
    # Por simplicidad, creamos un token con el user_id esperado

    user_ids = {
        "admin": 1,
        "manager": 2,
        "vendedor": 3,
        "viewer": 4,
        "auditor": 5,
    }

    role_map = {
        "admin": ["admin"],
        "manager": ["admin", "user"],
        "vendedor": ["user"],
        "viewer": ["viewer"],
        "auditor": ["user", "viewer"],
    }

    user_id = user_ids.get(username, 1)
    roles = role_map.get(username, ["viewer"])

    token_data = {"sub": str(user_id), "roles": roles}
    return create_access_token(token_data)


@pytest.fixture(scope="function")
def admin_headers() -> dict:
    """
    Headers de autenticacion para usuario admin.
    """
    token = get_auth_token("admin", "Northwind2024!")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def manager_headers() -> dict:
    """
    Headers de autenticacion para usuario manager (admin + user).
    """
    token = get_auth_token("manager", "Manager2024!")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def user_headers() -> dict:
    """
    Headers de autenticacion para usuario vendedor (user role).
    """
    token = get_auth_token("vendedor", "Vendedor2024!")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def viewer_headers() -> dict:
    """
    Headers de autenticacion para usuario viewer (solo lectura).
    """
    token = get_auth_token("viewer", "Viewer2024!")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def auditor_headers() -> dict:
    """
    Headers de autenticacion para usuario auditor (user + viewer).
    """
    token = get_auth_token("auditor", "Auditor2024!")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def auth_headers(admin_headers) -> dict:
    """
    Headers de autenticacion para usuario admin (fixture principal).
    """
    return admin_headers


# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================


@pytest.fixture
def sample_customer() -> dict:
    """
    Datos de ejemplo para crear un cliente.
    """
    return {
        "customer_id": "TEST1",
        "company_name": "Test Company",
        "contact_name": "John Doe",
        "contact_title": "Owner",
        "address": "123 Test Street",
        "city": "TestCity",
        "region": "TestRegion",
        "postal_code": "12345",
        "country": "TestCountry",
        "phone": "555-0100",
        "fax": "555-0101",
    }


@pytest.fixture
def sample_product() -> dict:
    """
    Datos de ejemplo para crear un producto.
    """
    return {
        "product_name": "Test Product",
        "supplier_id": 1,
        "category_id": 1,
        "quantity_per_unit": "10 boxes x 20 bags",
        "unit_price": 25.00,
        "units_in_stock": 100,
        "units_on_order": 0,
        "reorder_level": 10,
        "discontinued": 0,
    }


@pytest.fixture
def sample_order() -> dict:
    """
    Datos de ejemplo para crear una orden.
    """
    return {
        "customer_id": "ALFKI",
        "employee_id": 1,
        "ship_via": 1,
        "freight": 32.38,
        "ship_name": "Test Order",
        "ship_address": "123 Ship Street",
        "ship_city": "ShipCity",
        "ship_region": "ShipRegion",
        "ship_postal_code": "12345",
        "ship_country": "ShipCountry",
        "details": [
            {
                "product_id": 1,
                "unit_price": 18.00,
                "quantity": 10,
                "discount": 0,
            }
        ],
    }


@pytest.fixture
def sample_order_detail() -> dict:
    """
    Datos de ejemplo para un detalle de orden.
    """
    return {
        "product_id": 1,
        "unit_price": 18.00,
        "quantity": 10,
        "discount": 0,
    }
