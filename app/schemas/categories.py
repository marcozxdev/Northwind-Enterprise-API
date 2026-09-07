# schemas/categories.py
#
# Esquemas Pydantic para el recurso Categories (Categorias de productos).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de categorias.
#
# Esquemas esperados:
#
#   CategoryCreate (request body para POST):
#     - category_name: str              [requerido, max 15 caracteres]
#     - description:   str | None       [opcional, descripcion de la categoria]
#     - picture:       bytes | None     [opcional, imagen en bytes]
#
#   CategoryUpdate (request body para PUT/PATCH):
#     - Todos los campos de CategoryCreate pero opcionales.
#
#   CategoryResponse (response body):
#     - category_id:   int
#     - category_name: str
#     - description:   str | None
#     - Config: from_attributes = True
#
#   CategoryList:
#     - items: list[CategoryResponse]
#     - total: int
#
