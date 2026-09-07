# tests/test_customers.py
#
# Tests para los endpoints de Customers (Clientes).
#
# Archivos de endpoints que se testean: routers/customers.py
# Esquemas que se validan: schemas/customers.py
#
# Tests esperados:
#
#   test_listar_clientes():
#     - GET /api/customers retorna 200 y una lista.
#     - La respuesta tiene la estructura esperada (items, total, page, per_page).
#
#   test_obtener_cliente_por_id():
#     - GET /api/customers/{id} retorna 200 si el cliente existe.
#     - GET /api/customers/{id} retorna 404 si el cliente no existe.
#
#   test_crear_cliente():
#     - POST /api/customers con datos validos retorna 201.
#     - POST /api/customers con datos invalidos retorna 422.
#     - POST /api/customers con customer_id duplicado retorna 409.
#
#   test_actualizar_cliente():
#     - PUT /api/customers/{id} con datos validos retorna 200.
#     - PUT /api/customers/{id} inexistente retorna 404.
#
#   test_eliminar_cliente():
#     - DELETE /api/customers/{id} retorna 204 si existe.
#     - DELETE /api/customers/{id} inexistente retorna 404.
#
#   test_filtrar_clientes_por_pais():
#     - GET /api/customers?country=Germany retorna solo clientes de Alemania.
#
#   test_filtrar_clientes_por_ciudad():
#     - GET /api/customers?city=London retorna solo clientes de London.
#
