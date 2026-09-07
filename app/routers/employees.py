# routers/employees.py
#
# Endpoints para el recurso Employees (Empleados).
#
# Base de datos: tablas "employees" y "employee_territories"
#
# Endpoints esperados:
#
#   GET    /api/employees              -> Listar todos los empleados (con paginacion y filtros)
#   GET    /api/employees/{id}         -> Obtener un empleado por employee_id
#   POST   /api/employees              -> Crear un nuevo empleado
#   PUT    /api/employees/{id}         -> Actualizar un empleado existente
#   DELETE /api/employees/{id}         -> Eliminar un empleado
#   GET    /api/employees/{id}/territories -> Territorios asignados al empleado
#
# Filtros esperados en GET:
#   - last_name:   Filtrar por apellido
#   - first_name:  Filtrar por nombre
#   - title:       Filtrar por cargo
#   - country:     Filtrar por pais de residencia
#   - reports_to:  Filtrar por empleado jefe
#
# Esquchemas Pydantic (schemas/employees.py):
#   - EmployeeCreate:      Body para POST
#   - EmployeeUpdate:      Body para PUT (campos opcionales)
#   - EmployeeResponse:    Respuesta estandarizada
#   - EmployeeTerritory:   Respuesta de territorios asignados
#   - EmployeeList:        Respuesta paginada
#
# Modelo ORM (models/employees.py):
#   - Employee:          modelo que mapea la tabla "employees"
#   - EmployeeTerritory: modelo que mapea la tabla "employee_territories"
#
