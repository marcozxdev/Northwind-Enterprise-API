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
from typing import Optional

from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    """
    Cuerpo del request para POST /api/employees
    """
    last_name: str = Field(..., min_length=1, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=10)
    title: Optional[str] = Field(None, max_length=30)
    title_of_courtesy: Optional[str] = Field(None, max_length=25)
    birth_date: Optional[date] = None
    hire_date: Optional[date] = None
    address: Optional[str] = Field(None, max_length=60)
    city: Optional[str] = Field(None, max_length=15)
    region: Optional[str] = Field(None, max_length=15)
    postal_code: Optional[str] = Field(None, max_length=10)
    country: Optional[str] = Field(None, max_length=15)
    home_phone: Optional[str] = Field(None, max_length=24)
    extension: Optional[str] = Field(None, max_length=4)
    notes: Optional[str] = None
    reports_to: Optional[int] = None
    photo_path: Optional[str] = Field(None, max_length=255)


class EmployeeUpdate(BaseModel):
    """Todos los campos opcionales para PUT /api/employees/{employee_id}"""
    last_name: Optional[str] = Field(None, max_length=20)
    first_name: Optional[str] = Field(None, max_length=10)
    title: Optional[str] = Field(None, max_length=30)
    title_of_courtesy: Optional[str] = Field(None, max_length=25)
    birth_date: Optional[date] = None
    hire_date: Optional[date] = None
    address: Optional[str] = Field(None, max_length=60)
    city: Optional[str] = Field(None, max_length=15)
    region: Optional[str] = Field(None, max_length=15)
    postal_code: Optional[str] = Field(None, max_length=10)
    country: Optional[str] = Field(None, max_length=15)
    home_phone: Optional[str] = Field(None, max_length=24)
    extension: Optional[str] = Field(None, max_length=4)
    notes: Optional[str] = None
    reports_to: Optional[int] = None
    photo_path: Optional[str] = Field(None, max_length=255)


class EmployeeTerritoryResponse(BaseModel):
    """
    Respuesta de un territorio asignado a un empleado.
    """
    employee_id: int
    territory_id: str
    territory_description: Optional[str] = None

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
    title: Optional[str]
    title_of_courtesy: Optional[str]
    birth_date: Optional[date]
    hire_date: Optional[date]
    address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    home_phone: Optional[str]
    extension: Optional[str]
    notes: Optional[str]
    reports_to: Optional[int]
    photo_path: Optional[str]
    reports_to_name: Optional[str] = None

    model_config = {"from_attributes": True}


class EmployeeList(BaseModel):
    """Respuesta paginada de empleados."""
    items: list[EmployeeResponse]
    total: int
    page: int
    per_page: int
