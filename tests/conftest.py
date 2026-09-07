# tests/conftest.py
#
# Configuracion compartida de pytest (fixtures).
#
# Este archivo contiene los fixtures que se usan en todos los tests.
# Pytest los carga automaticamente antes de cada test que los necesite.
#
# Fixtures esperados:
#
#   client():
#     - Crea un TestClient de FastAPI apuntando a la app.
#     - Se usa para hacer peticiones HTTP simuladas.
#     - Ej: response = client.get("/api/customers")
#
#   db_session():
#     - Crea una sesion de BD en memoria (SQLite) para tests.
#     - Cada test empieza con la BD limpia (rollback automatico).
#     - No depende de PostgreSQL real.
#
#   sample_customer():
#     - Retorna un diccionario con datos de ejemplo de un cliente.
#     - Se usa para crear registros de prueba en los tests.
#     - Ej: {"customer_id": "TEST1", "company_name": "Test Company"}
#
#   sample_product():
#     - Retorna un diccionario con datos de ejemplo de un producto.
#
#   sample_order():
#     - Retorna un diccionario con datos de ejemplo de una orden.
#
# Ejemplo de uso:
#
#   def test_listar_clientes(client):
#       response = client.get("/api/customers")
#       assert response.status_code == 200
#
#   def test_crear_cliente(client, sample_customer):
#       response = client.post("/api/customers", json=sample_customer)
#       assert response.status_code == 201
#
