# tests/test_products.py
#
# Tests para los endpoints de Products (Productos).
#
# Archivos de endpoints que se testean: routers/products.py
# Esquemas que se validan: schemas/products.py
#
# Tests esperados:
#
#   test_listar_productos():
#     - GET /api/products retorna 200 y una lista paginada.
#
#   test_obtener_producto_por_id():
#     - GET /api/products/{id} retorna 200 si el producto existe.
#     - GET /api/products/{id} retorna 404 si no existe.
#
#   test_crear_producto():
#     - POST /api/products con datos validos retorna 201.
#     - POST /api/products sin product_name retorna 422 (campo requerido).
#
#   test_actualizar_producto():
#     - PUT /api/products/{id} retorna 200 si existe.
#     - PUT /api/products/{id} inexistente retorna 404.
#
#   test_eliminar_producto():
#     - DELETE /api/products/{id} retorna 204 si existe.
#     - DELETE /api/products/{id} inexistente retorna 404.
#
#   test_filtrar_por_categoria():
#     - GET /api/products?category_id=1 retorna solo productos de esa categoria.
#
#   test_filtrar_por_proveedor():
#     - GET /api/products?supplier_id=1 retorna solo productos de ese proveedor.
#
#   test_filtrar_por_precio():
#     - GET /api/products?price_min=10&price_max=50 retorna productos en ese rango.
#
#   test_producto_inactivo():
#     - GET /api/products?discontinued=1 retorna solo productos descontinuados.
#
