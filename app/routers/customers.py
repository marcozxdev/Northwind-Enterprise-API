# routers/customers.py
#
# Endpoints para el recurso Customers (Clientes).
#
# Base de datos: tabla "customers"
#
# Endpoints esperados:
#
#   GET    /api/customers          -> Listar todos los clientes (con paginacion y filtros)
#   GET    /api/customers/{id}     -> Obtener un cliente por su customer_id (ej: "ALFKI")
#   POST   /api/customers          -> Crear un nuevo cliente
#   PUT    /api/customers/{id}     -> Actualizar un cliente existente
#   DELETE /api/customers/{id}     -> Eliminar un cliente
#
# Filtros esperados en GET:
#   - company_name:  Filtrar por nombre de empresa (busqueda parcial)
#   - city:          Filtrar por ciudad
#   - country:       Filtrar por pais
#   - contact_title: Filtrar por cargo del contacto
#
# Esquemas Pydantic (schemas/customers.py):
#   - CustomerCreate:   Body para POST
#   - CustomerUpdate:   Body para PUT (campos opcionales)
#   - CustomerResponse: Respuesta estandarizada
#   - CustomerList:     Respuesta paginada
#
# Modelo ORM (models/customers.py):
#   - Customer: modelo que mapea la tabla "customers"
#
