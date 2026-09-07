# routers/shippers.py
#
# Endpoints para el recurso Shippers (Transportistas).
#
# Base de datos: tabla "shippers"
#
# Endpoints esperados:
#
#   GET    /api/shippers            -> Listar todos los transportistas
#   GET    /api/shippers/{id}       -> Obtener un transportista por shipper_id
#   POST   /api/shippers            -> Crear un nuevo transportista
#   PUT    /api/shippers/{id}       -> Actualizar un transportista existente
#   DELETE /api/shippers/{id}       -> Eliminar un transportista
#
# Notas:
#   - Son pocos registros (3 en Northwind: Speedy Express, United Package, Federal Shipping).
#   - No se esperan filtros complejos.
#
# Esquemas Pydantic (schemas/shippers.py):
#   - ShipperCreate:   Body para POST
#   - ShipperUpdate:   Body para PUT (campos opcionales)
#   - ShipperResponse: Respuesta estandarizada
#   - ShipperList:     Lista de transportistas
#
# Modelo ORM (models/shippers.py):
#   - Shipper: modelo que mapea la tabla "shippers"
#
