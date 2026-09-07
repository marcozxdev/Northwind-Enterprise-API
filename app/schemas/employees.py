# schemas/employees.py
#
# Esquemas Pydantic para el recurso Employees (Empleados).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de empleados.
#
# Esquemas esperados:
#
#   EmployeeCreate (request body para POST):
#     - last_name:          str              [requerido]
#     - first_name:         str              [requerido]
#     - title:              str | None       [opcional, cargo]
#     - title_of_courtesy:  str | None       [opcional, "Mr.", "Ms.", "Dr.", etc.]
#     - birth_date:         date | None      [opcional, fecha de nacimiento]
#     - hire_date:          date | None      [opcional, fecha de contratacion]
#     - address:            str | None       [opcional]
#     - city:               str | None       [opcional]
#     - region:             str | None       [opcional]
#     - postal_code:        str | None       [opcional]
#     - country:            str | None       [opcional]
#     - home_phone:         str | None       [opcional, telefono]
#     - extension:          str | None       [opcional, extension]
#     - notes:              str | None       [opcional, notas biograficas]
#     - reports_to:         int | None       [opcional, employee_id del jefe]
#     - photo_path:         str | None       [opcional, URL de foto]
#
#   EmployeeUpdate (request body para PUT/PATCH):
#     - Todos los campos de EmployeeCreate pero opcionales.
#
#   EmployeeResponse (response body):
#     - Todos los campos de la tabla employees.
#     - Incluye reports_to_name: str | None (nombre del jefe, join)
#     - Config: from_attributes = True
#
#   EmployeeTerritoryResponse:
#     - employee_id:   int
#     - territory_id:  str
#     - territory_description: str (join con territories)
#
#   EmployeeList (respuesta paginada):
#     - items:    list[EmployeeResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
