# models/employees.py
#
# Modelos ORM SQLAlchemy para las tablas "employees" y "employee_territories".
#
# Tabla: employees
# Descripcion: Empleados de la empresa Northwind.
#
# Columnas de employees:
#   - employee_id:        SMALLINT      PK, identificador unico del empleado
#   - last_name:          VARCHAR(20)   NOT NULL, apellido
#   - first_name:         VARCHAR(10)   NOT NULL, nombre
#   - title:              VARCHAR(30)   cargo (ej: "Sales Representative")
#   - title_of_courtesy:  VARCHAR(25)   trato (ej: "Mr.", "Ms.", "Dr.")
#   - birth_date:         DATE          fecha de nacimiento
#   - hire_date:          DATE          fecha de contratacion
#   - address:            VARCHAR(60)   direccion personal
#   - city:               VARCHAR(15)   ciudad
#   - region:             VARCHAR(15)   region/estado
#   - postal_code:        VARCHAR(10)   codigo postal
#   - country:            VARCHAR(15)   pais
#   - home_phone:         VARCHAR(24)   telefono personal
#   - extension:          VARCHAR(4)    extension de oficina
#   - photo:              BYTEA         foto del empleado (bytes)
#   - notes:              TEXT          notas biograficas
#   - reports_to:         SMALLINT      FK -> employees.employee_id (jefe directo)
#   - photo_path:         VARCHAR(255)  URL de la foto
#
# Relaciones de employees:
#   - manager:       Relationship con Employee (self-referencial, reports_to)
#   - subordinates:  Relationship con Employee (empleados que reportan a este)
#   - orders:        Relationship con Order (un empleado -> muchas ordenes)
#   - territories:   Relationship con Territory (via employee_territories)
#
# Tabla: employee_territories
# Descripcion: Tabla asociativa entre empleados y territorios.
#
# Columnas de employee_territories:
#   - employee_id:   SMALLINT    PK, FK -> employees.employee_id
#   - territory_id:  VARCHAR(20) PK, FK -> territories.territory_id
#
# Relaciones de employee_territories:
#   - employee:  Relationship con Employee
#   - territory: Relationship con Territory
#
