# tests/test_orders.py
#
# Tests para los endpoints de Orders (Ordenes).
#
# Archivos de endpoints que se testean: routers/orders.py
# Esquemas que se validan: schemas/orders.py
#
# Tests esperados:
#
#   test_listar_ordenes():
#     - GET /api/orders retorna 200 y una lista paginada.
#
#   test_obtener_orden_por_id():
#     - GET /api/orders/{id} retorna 200 si la orden existe.
#     - GET /api/orders/{id} retorna 404 si la orden no existe.
#     - La respuesta incluye los detalles de la orden (order_details).
#
#   test_crear_orden():
#     - POST /api/orders con datos validos retorna 201.
#     - POST /api/orders con detalles retorna 201 y los detalles se guardan.
#
#   test_actualizar_orden():
#     - PUT /api/orders/{id} retorna 200 si existe.
#     - PUT /api/orders/{id} inexistente retorna 404.
#
#   test_eliminar_orden():
#     - DELETE /api/orders/{id} retorna 204 si existe.
#     - DELETE /api/orders/{id} inexistente retorna 404.
#
#   test_filtrar_ordenes_por_cliente():
#     - GET /api/orders?customer_id=ALFKI retorna solo ordenes de ese cliente.
#
#   test_filtrar_ordenes_por_fecha():
#     - GET /api/orders?date_from=1996-07-01&date_to=1996-07-31 retorna ordenes de ese rango.
#
#   test_crear_orden_sin_cliente():
#     - POST /api/orders sin customer_id retorna 400 (validacion de regla de negocio).
#
