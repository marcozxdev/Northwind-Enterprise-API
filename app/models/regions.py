# app/models/regions.py
#
# Modelos ORM SQLAlchemy para las tablas "region", "territories" y "us_states".
#
# ============================================================================
# TABLA: region
# ============================================================================
# Descripcion: Regiones geograficas (Eastern, Western, Northern, Southern).
#
# Columnas:
#   - region_id:            SMALLSERIAL PK, identificador unico de la region
#   - region_description:   VARCHAR(60) NOT NULL, descripcion de la region
#
# Relaciones:
#   - territories -> Territory (1:N)
#     Una region contiene muchos territorios.
#
# ============================================================================
# TABLA: territories
# ============================================================================
# Descripcion: Territorios especificos dentro de cada region.
#
# Columnas:
#   - territory_id:            VARCHAR(20) PK, identificador del territorio
#   - territory_description:   VARCHAR(60) NOT NULL, descripcion del territorio
#   - region_id:               SMALLINT    FK -> region.region_id
#
# Relaciones:
#   - region -> Region (N:1)
#     Un territorio pertenece a una region.
#   - employees -> Employee (M:N via employee_territories)
#     Un territorio puede estar asignado a varios empleados.
#
# ============================================================================
# TABLA: us_states
# ============================================================================
# Descripcion: Estados de Estados Unidos (para referencia geografica).
#
# Columnas:
#   - state_id:      SMALLSERIAL PK, identificador del estado
#   - state_name:    VARCHAR(100) nombre del estado
#   - state_abbr:    VARCHAR(2)   abreviatura (ej: "WA", "CA")
#   - state_region:  VARCHAR(50)  region del estado
#
# Notas:
#   - Tabla de referencia, no tiene relaciones con otras tablas.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener todas las regiones con sus territorios:
#   regiones = db.query(Region).options(
#       selectinload(Region.territories)
#   ).all()
#
#   # Obtener un territorio con su region:
#   territorio = db.query(Territory).options(
#       selectinload(Territory.region)
#   ).filter(Territory.territory_id == "06897").first()
#
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Region(Base):
    __tablename__ = "region"

    region_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    region_description: Mapped[str] = mapped_column(String(60), nullable=False)

    # Relaciones
    territories: Mapped[list["Territory"]] = relationship(
        "Territory",
        back_populates="region",
    )

    def __repr__(self) -> str:
        return f"<Region {self.region_id}: {self.region_description}>"


class Territory(Base):
    __tablename__ = "territories"

    territory_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    territory_description: Mapped[str] = mapped_column(String(60), nullable=False)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.region_id"))

    # Relaciones
    region: Mapped["Region"] = relationship("Region", back_populates="territories")
    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        secondary="employee_territories",
        back_populates="territories",
    )

    def __repr__(self) -> str:
        return f"<Territory {self.territory_id}: {self.territory_description}>"


class UsState(Base):
    __tablename__ = "us_states"

    state_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    state_name: Mapped[str | None] = mapped_column(String(100))
    state_abbr: Mapped[str | None] = mapped_column(String(2))
    state_region: Mapped[str | None] = mapped_column(String(50))

    def __repr__(self) -> str:
        return f"<UsState {self.state_id}: {self.state_name}>"
