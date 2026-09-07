# routers/products.py
#
# Endpoints para el recurso Products (Productos).
#
# Base de datos: tabla "products"
#
# Endpoints esperados:
#
#   GET    /api/products          -> Listar todos los productos (con paginacion y filtros)
#   GET    /api/products/{id}     -> Obtener un producto por product_id
#   POST   /api/products          -> Crear un nuevo producto
#   PUT    /api/products/{id}     -> Actualizar un producto existente
#   DELETE /api/products/{id}     -> Eliminar un producto
#
# Filtros esperados en GET:
#   - category_id:    Filtrar por categoria
#   - supplier_id:    Filtrar por proveedor
#   - discontinuated: Filtrar por estado (activo/inactivo)
#   - price_min:      Filtrar por precio minimo
#   - price_max:      Filtrar por precio maximo
#   - in_stock:       Filtrar solo productos con stock disponible
#
# Esquemas Pydantic (schemas/products.py):
#   - ProductCreate:   Body para POST
#   - ProductUpdate:   Body para PUT (campos opcionales)
#   - ProductResponse: Respuesta estandarizada (incluye nombre de categoria y proveedor)
#   - ProductList:     Respuesta paginada
#
# Modelo ORM (models/products.py):
#   - Product: modelo que mapea la tabla "products"
#
