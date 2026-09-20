# app/routers/employees.py
#
# Endpoints para el recurso Employees (Empleados).
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET    /api/employees              -> Listar empleados (con filtros)
#   GET    /api/employees/{id}         -> Obtener un empleado
#   POST   /api/employees              -> Crear un empleado
#   PUT    /api/employees/{id}         -> Actualizar un empleado
#   DELETE /api/employees/{id}         -> Eliminar un empleado
#   GET    /api/employees/{id}/territories -> Territorios del empleado
#
# ============================================================================
# CACHE
# ============================================================================
#
#   GET endpoints usan Redis cache con TTL de 3 min (list) y 5 min (detail).
#   POST/PUT/DELETE invalidan el cache de employees.
#
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.cache import cache_response, delete_cache_pattern
from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.users import User
from app.repositories.employees import EmployeeRepository
from app.schemas.employees import (
    EmployeeCreate,
    EmployeeList,
    EmployeeResponse,
    EmployeeTerritoryResponse,
    EmployeeUpdate,
)

router = APIRouter(prefix="/employees", tags=["Empleados"])


@router.get("/", response_model=EmployeeList)
@cache_response(ttl=180, prefix="employees:list")
def list_employees(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    last_name: Optional[str] = None,
    first_name: Optional[str] = None,
    title: Optional[str] = None,
    country: Optional[str] = None,
    reports_to: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Lista empleados con filtros opcionales.

    GET /api/employees?page=1&country=USA

    Cache: 180 segundos (3 min)
    """
    repo = EmployeeRepository(db)
    items, total = repo.get_all_with_filters(
        page=page,
        per_page=per_page,
        last_name=last_name,
        first_name=first_name,
        title=title,
        country=country,
        reports_to=reports_to,
    )

    enriched_items = []
    for emp in items:
        resp = EmployeeResponse.model_validate(emp)
        if emp.manager:
            resp.reports_to_name = f"{emp.manager.first_name} {emp.manager.last_name}"
        enriched_items.append(resp)

    return EmployeeList(items=enriched_items, total=total, page=page, per_page=per_page)


@router.get("/{employee_id}", response_model=EmployeeResponse)
@cache_response(ttl=300, prefix="employees:get")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene un empleado por ID.

    GET /api/employees/{employee_id}

    Cache: 300 segundos (5 min)
    """
    repo = EmployeeRepository(db)
    employee = repo.get_with_relations(employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado",
        )

    response = EmployeeResponse.model_validate(employee)
    if employee.manager:
        response.reports_to_name = f"{employee.manager.first_name} {employee.manager.last_name}"

    return response


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Crea un nuevo empleado.

    POST /api/employees

    Invalida cache de employees.
    """
    repo = EmployeeRepository(db)
    new_employee = repo.create(data.model_dump())

    delete_cache_pattern("employees:*")

    return new_employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user"])),
):
    """
    Actualiza un empleado.

    PUT /api/employees/{employee_id}

    Invalida cache de employees.
    """
    repo = EmployeeRepository(db)

    employee = repo.get_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado",
        )

    updated = repo.update(employee_id, data.model_dump(exclude_unset=True))

    delete_cache_pattern("employees:*")

    return updated


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"])),
):
    """
    Elimina un empleado.

    DELETE /api/employees/{employee_id}

    Invalida cache de employees.
    """
    repo = EmployeeRepository(db)

    employee = repo.get_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado",
        )

    repo.delete(employee_id)

    delete_cache_pattern("employees:*")

    return None


@router.get("/{employee_id}/territories", response_model=list[EmployeeTerritoryResponse])
def get_employee_territories(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "user", "viewer"])),
):
    """
    Obtiene los territorios asignados a un empleado.

    GET /api/employees/{employee_id}/territories
    """
    repo = EmployeeRepository(db)
    employee = repo.get_with_territories(employee_id)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado",
        )

    territories = []
    for terr in employee.territories:
        territories.append(
            EmployeeTerritoryResponse(
                employee_id=employee_id,
                territory_id=terr.territory_id,
                territory_description=terr.territory_description,
            )
        )

    return territories
