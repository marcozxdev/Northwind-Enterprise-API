# routers/categories.py
#
# Endpoints para el recurso Categories (Categorias de productos).
#
# Base de datos: tabla "categories"
#
# Endpoints esperados:
#
#   GET    /api/categories          -> Listar todas las categorias
#   GET    /api/categories/{id}     -> Obtener una categoria por category_id
#   POST   /api/categories          -> Crear una nueva categoria
#   PUT    /api/categories/{id}     -> Actualizar una categoria existente
#   DELETE /api/categories/{id}     -> Eliminar una categoria
#
# Notas:
#   - Las categorias son pocas (8 registros en Northwind).
#   - No se esperan filtros complejos, solo busqueda por nombre.
#
# Esquemas Pydantic (schemas/categories.py):
#   - CategoryCreate:   Body para POST
#   - CategoryUpdate:   Body para PUT (campos opcionales)
#   - CategoryResponse: Respuesta estandarizada
#   - CategoryList:     Lista de categorias
#
# Modelo ORM (models/categories.py):
#   - Category: modelo que mapea la tabla "categories"
#
