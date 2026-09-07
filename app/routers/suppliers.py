# routers/suppliers.py
#
# Endpoints para el recurso Suppliers (Proveedores).
#
# Base de datos: tabla "suppliers"
#
# Endpoints esperados:
#
#   GET    /api/suppliers          -> Listar todos los proveedores (con paginacion y filtros)
#   GET    /api/suppliers/{id}     -> Obtener un proveedor por supplier_id
#   POST   /api/suppliers          -> Crear un nuevo proveedor
#   PUT    /api/suppliers/{id}     -> Actualizar un proveedor existente
#   DELETE /api/suppliers/{id}     -> Eliminar un proveedor
#
# Filtros esperados en GET:
#   - country:  Filtrar por pais del proveedor
#   - city:     Filtrar por ciudad
#   - company_name: Filtrar por nombre de empresa
#
# Esquemas Pydantic (schemas/suppliers.py):
#   - SupplierCreate:   Body para POST
#   - SupplierUpdate:   Body para PUT (campos opcionales)
#   - SupplierResponse: Respuesta estandarizada
#   - SupplierList:     Respuesta paginada
#
# Modelo ORM (models/suppliers.py):
#   - Supplier: modelo que mapea la tabla "suppliers"
#
