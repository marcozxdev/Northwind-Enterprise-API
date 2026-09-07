# schemas/products.py
#
# Esquemas Pydantic para el recurso Products (Productos).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de productos.
#
# Esquemas esperados:
#
#   ProductCreate (request body para POST):
#     - product_name:       str              [requerido]
#     - supplier_id:        int | None       [opcional, proveedor]
#     - category_id:        int | None       [opcional, categoria]
#     - quantity_per_unit:  str | None       [opcional, ej: "10 boxes x 20 bags"]
#     - unit_price:         float | None     [opcional, precio unitario]
#     - units_in_stock:     int | None       [opcional, stock actual]
#     - units_on_order:     int | None       [opcional, unidades en pedido]
#     - reorder_level:      int | None       [opcional, nivel de reorden]
#     - discontinued:       int              [requerido, 0=activo, 1=inactivo]
#
#   ProductUpdate (request body para PUT/PATCH):
#     - Todos los campos de ProductCreate pero opcionales.
#
#   ProductResponse (response body):
#     - Todos los campos de la tabla products.
#     - Incluye category_name: str | None (nombre de la categoria, join)
#     - Incluye supplier_company: str | None (nombre del proveedor, join)
#     - Config: from_attributes = True
#
#   ProductList (respuesta paginada):
#     - items:    list[ProductResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
