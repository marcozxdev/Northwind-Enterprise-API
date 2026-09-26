# app/schemas/employees.py
#
# Esquemas Pydantic para el recurso Employees (Empleados).
#
# ============================================================================
# ESQUEMAS
# ============================================================================
#
#   EmployeeCreate (request body para POST):
#     - last_name:          str  [requerido]
#     - first_name:         str  [requerido]
#     - title:              str | None [opcional]
#     - title_of_courtesy:  str | None [opcional]
#     - birth_date:         date | None [opcional]
#     - hire_date:          date | None [opcional]
#     - address:            str | None [opcional]
#     - city:               str | None [opcional]
#     - region:             str | None [opcional]
#     - postal_code:        str | None [opcional]
#     - country:            str | None [opcional]
#     - home_phone:         str | None [opcional]
#     - extension:          str | None [opcional]
#     - notes:              str | None [opcional]
#     - reports_to:         int | None [opcional]
#     - photo_path:         str | None [opcional]
#
#   EmployeeUpdate (request body para PUT/PATCH):
#     - Todos los campos de EmployeeCreate pero opcionales.
#
#   EmployeeResponse (response body):
#     - Todos los campos de la tabla employees.
#     - reports_to_name: str | None (nombre del jefe, join)
#
#   EmployeeTerritoryResponse:
#     - employee_id, territory_id, territory_description
#
#   EmployeeList (respuesta paginada):
#     - items, total, page, per_page
#
from datetime import date

from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    """
    Cuerpo del request para POST /api/employees
    """
    last_name: str = Field(..., min_length=1, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=10)
    title: str | None = Field(None, max_length=30)
    title_of_courtesy: str | None = Field(None, max_length=25)
    birth_date: date | None = None
    hire_date: date | None = None
    address: str | None = Field(None, max_length=60)
    city: str | None = Field(None, max_length=15)
    region: str | None = Field(None, max_length=15)
    postal_code: str | None = Field(None, max_length=10)
    country: str | None = Field(None, max_length=15)
    home_phone: str | None = Field(None, max_length=24)
    extension: str | None = Field(None, max_length=4)
    notes: str | None = None
    reports_to: int | None = None
    photo_path: str | None = Field(None, max_length=255)


class EmployeeUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/employees/{employee_id}"""
    last_name: str | None = Field(None, max_length=20)
    first_name: str | None = Field(None, max_length=10)
    title: str | None = Field(None, max_length=30)
    title_of_courtesy: str | None = Field(None, max_length=25)
    birth_date: date | None = None
    hire_date: date | None = None
    address: str | None = Field(None, max_length=60)
    city: str | None = Field(None, max_length=15)
    region: str | None = Field(None, max_length=15)
    postal_code: str | None = Field(None, max_length=10)
    country: str | None = Field(None, max_length=15)
    home_phone: str | None = Field(None, max_length=24)
    extension: str | None = Field(None, max_length=4)
    notes: str | None = None
    reports_to: int | None = None
    photo_path: str | None = Field(None, max_length=255)


class EmployeeTerritoryResponse(BaseModel):
    """
    Respuesta de un territorio asignado a un empleado.
    """
    employee_id: int
    territory_id: str
    territory_description: str | None = None

    model_config = {"from_attributes": True}


class EmployeeResponse(BaseModel):
    """
    Respuesta de un empleado.

    Incluye:
        - Todos los campos de la tabla employees
        - reports_to_name: str | None (nombre del jefe)
    """
    employee_id: int
    last_name: str
    first_name: str
    title: str | None
    title_of_courtesy: str | None
    birth_date: date | None
    hire_date: date | None
    address: str | None
    city: str | None
    region: str | None
    postal_code: str | None
    country: str | None
    home_phone: str | None
    extension: str | None
    notes: str | None
    reports_to: int | None
    photo_path: str | None
    reports_to_name: str | None = None

    model_config = {"from_attributes": True}


class EmployeeList(BaseModel):
    """Respuesta paginada de empleados."""
    items: list[EmployeeResponse]
    total: int
    page: int
    per_page: int
