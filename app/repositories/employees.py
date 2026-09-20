# app/repositories/employees.py
#
# Repository para el modelo Employee.
#
# ============================================================================
# METODOS ESPECIFICOS
# ============================================================================
#
#   get_with_relations(employee_id):
#     - Obtiene un empleado con su jefe y subordinados
#
#   get_with_territories(employee_id):
#     - Obtiene un empleado con sus territorios asignados
#
#   get_all_with_filters(last_name, first_name, title, country, reports_to):
#     - Lista empleados con filtros opcionales
#
from typing import List, Optional

from sqlalchemy.orm import Session, selectinload

from app.models.employees import Employee
from app.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    """
    Repository para el modelo Employee.

    Hereda: get_by_id(), get_all(), create(), update(), delete(), count()
    """

    def __init__(self, db: Session):
        super().__init__(Employee, db)

    def get_with_relations(self, employee_id: int) -> Optional[Employee]:
        """
        Obtiene un empleado con su jefe y subordinados.

        Args:
            employee_id: ID del empleado

        Returns:
            Employee | None: Empleado con relaciones o None
        """
        return self.db.query(Employee).options(
            selectinload(Employee.manager),
            selectinload(Employee.subordinates),
        ).filter(Employee.employee_id == employee_id).first()

    def get_with_territories(self, employee_id: int) -> Optional[Employee]:
        """
        Obtiene un empleado con sus territorios asignados.

        Args:
            employee_id: ID del empleado

        Returns:
            Employee | None: Empleado con territorios o None
        """
        return self.db.query(Employee).options(
            selectinload(Employee.territories)
        ).filter(Employee.employee_id == employee_id).first()

    def get_all_with_filters(
        self,
        page: int = 1,
        per_page: int = 10,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        title: Optional[str] = None,
        country: Optional[str] = None,
        reports_to: Optional[int] = None,
    ) -> tuple[List[Employee], int]:
        """
        Obtiene empleados con filtros.

        Args:
            page: Pagina
            per_page: Registros por pagina
            last_name: Filtrar por apellido
            first_name: Filtrar por nombre
            title: Filtrar por cargo
            country: Filtrar por pais
            reports_to: Filtrar por jefe directo

        Returns:
            tuple: (lista de empleados, total)
        """
        query = self.db.query(Employee).options(
            selectinload(Employee.manager)
        )

        if last_name:
            query = query.filter(Employee.last_name.ilike(f"%{last_name}%"))
        if first_name:
            query = query.filter(Employee.first_name.ilike(f"%{first_name}%"))
        if title:
            query = query.filter(Employee.title.ilike(f"%{title}%"))
        if country:
            query = query.filter(Employee.country.ilike(f"%{country}%"))
        if reports_to is not None:
            query = query.filter(Employee.reports_to == reports_to)

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return items, total
