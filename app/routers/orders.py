# routers/orders.py
#
# Endpoints para el recurso Orders (Ordenes de compra).
#
# Base de datos: tablas "orders" y "order_details"
#
# Endpoints esperados:
#
#   GET    /api/orders                    -> Listar todas las ordenes (con paginacion y filtros)
#   GET    /api/orders/{id}               -> Obtener una orden por order_id (ej: 10248)
#   POST   /api/orders                    -> Crear una orden nueva (con detalles)
#   PUT    /api/orders/{id}               -> Actualizar una orden existente
#   DELETE /api/orders/{id}               -> Eliminar una orden
#   GET    /api/orders/{id}/details       -> Obtener los detalles de una orden
#
# Filtros esperados en GET:
#   - customer_id:  Filtrar por cliente
#   - employee_id:  Filtrar por empleado que tomo la orden
#   - date_from:    Filtrar ordenes desde una fecha
#   - date_to:      Filtrar ordenes hasta una fecha
#   - shipped:      Filtrar por estado de envio (enviado/pendiente)
#
# Esquemas Pydantic (schemas/orders.py):
#   - OrderCreate:        Body para POST
#   - OrderUpdate:        Body para PUT (campos opcionales)
#   - OrderResponse:      Respuesta estandarizada
#   - OrderDetailCreate:  Body para detalles de orden
#   - OrderDetailResponse: Respuesta de detalles
#   - OrderList:          Respuesta paginada
#
# Modelo ORM (models/orders.py):
#   - Order:        modelo que mapea la tabla "orders"
#   - OrderDetail:  modelo que mapea la tabla "order_details"
#
