# app/models/employees.py
#
# Modelos ORM SQLAlchemy para las tablas "employees" y "employee_territories".
#
# ============================================================================
# TABLA: employees
# ============================================================================
# Descripcion: Empleados de la empresa Northwind.
#
# Columnas:
#   - employee_id:        SMALLSERIAL PK, identificador unico del empleado
#   - last_name:          VARCHAR(20) NOT NULL, apellido
#   - first_name:         VARCHAR(10) NOT NULL, nombre
#   - title:              VARCHAR(30) cargo (ej: "Sales Representative")
#   - title_of_courtesy:  VARCHAR(25) trato (ej: "Mr.", "Ms.", "Dr.")
#   - birth_date:         DATE        fecha de nacimiento
#   - hire_date:          DATE        fecha de contratacion
#   - address:            VARCHAR(60) direccion personal
#   - city:               VARCHAR(15) ciudad
#   - region:             VARCHAR(15) region/estado
#   - postal_code:        VARCHAR(10) codigo postal
#   - country:            VARCHAR(15) pais
#   - home_phone:         VARCHAR(24) telefono personal
#   - extension:          VARCHAR(4)  extension de oficina
#   - photo:              BYTEA       foto del empleado (bytes)
#   - notes:              TEXT        notas biograficas
#   - reports_to:         SMALLINT    FK -> employees.employee_id (jefe directo)
#   - photo_path:         VARCHAR(255) URL de la foto
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   manager -> Employee (N:1, self-referencial via reports_to)
#     Un empleado tiene un jefe (reports_to = employee_id del jefe).
#     Andrew Fuller (ID=2) no tiene jefe (reports_to = NULL).
#
#   subordinates -> Employee (1:N, self-referencial inverso)
#     Un empleado puede tener varios subordinados.
#
#   orders -> Order (1:N)
#     Un empleado puede tomar muchas ordenes.
#
#   territories -> Territory (M:N via employee_territories)
#     Un empleado puede estar asignado a varios territorios.
#
# ============================================================================
# TABLA: employee_territories
# ============================================================================
# Descripcion: Tabla asociativa entre empleados y territorios.
#
# Columnas:
#   - employee_id:   SMALLINT    PK, FK -> employees.employee_id
#   - territory_id:  VARCHAR(20) PK, FK -> territories.territory_id
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener un empleado con su jefe:
#   empleado = db.query(Employee).options(
#       selectinload(Employee.manager)
#   ).filter(Employee.employee_id == 1).first()
#   # empleado.manager = Andrew Fuller (el jefe de Nancy Davolio)
#
#   # Obtener un empleado con sus subordinados:
#   jefe = db.query(Employee).options(
#       selectinload(Employee.subordinates)
#   ).filter(Employee.employee_id == 2).first()
#   # jefe.subordinates = [Nancy, Janet, Margaret, Laura]
#
#   # Obtener un empleado con sus territorios:
#   empleado = db.query(Employee).options(
#       selectinload(Employee.territories)
#   ).filter(Employee.employee_id == 1).first()
#   # empleado.territories = [Territory("06897"), Territory("19713")]
#
from datetime import date

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# Tabla asociativa employee_territories
# SQLAlchemy la usa como tabla "secondary" en la relacion M:N
employee_territories = EmployeeTerritory.__table__ if False else None
# Se define aqui para que los modelos la encuentren al importar


class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str | None] = mapped_column(String(30))
    title_of_courtesy: Mapped[str | None] = mapped_column(String(25))
    birth_date: Mapped[date | None] = mapped_column()
    hire_date: Mapped[date | None] = mapped_column()
    address: Mapped[str | None] = mapped_column(String(60))
    city: Mapped[str | None] = mapped_column(String(15))
    region: Mapped[str | None] = mapped_column(String(15))
    postal_code: Mapped[str | None] = mapped_column(String(10))
    country: Mapped[str | None] = mapped_column(String(15))
    home_phone: Mapped[str | None] = mapped_column(String(24))
    extension: Mapped[str | None] = mapped_column(String(4))
    photo: Mapped[bytes | None] = mapped_column(default=None)
    notes: Mapped[str | None] = mapped_column(Text)
    reports_to: Mapped[int | None] = mapped_column(ForeignKey("employees.employee_id"))
    photo_path: Mapped[str | None] = mapped_column(String(255))

    # Relaciones
    manager: Mapped["Employee | None"] = relationship(
        "Employee",
        remote_side="Employee.employee_id",
        back_populates="subordinates",
    )
    subordinates: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="manager",
    )
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="employee",
    )
    territories: Mapped[list["Territory"]] = relationship(
        "Territory",
        secondary="employee_territories",
        back_populates="employees",
    )

    def __repr__(self) -> str:
        return f"<Employee {self.employee_id}: {self.first_name} {self.last_name}>"


# Tabla asociativa employee_territories
# Define la relacion M:N entre employees y territories
EmployeeTerritory = Table(
    "employee_territories",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.employee_id"), primary_key=True),
    Column("territory_id", ForeignKey("territories.territory_id"), primary_key=True),
)
