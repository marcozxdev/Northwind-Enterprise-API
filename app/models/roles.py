# app/models/roles.py
#
# Modelo ORM SQLAlchemy para la tabla "roles".
#
# ============================================================================
# TABLA: roles
# ============================================================================
# Descripcion: Catalogo de roles del sistema de autorizacion.
#
# Cada rol define un nivel de permisos en la API:
#   - admin:  Acceso completo CRUD a todos los recursos
#   - user:   Lectura y escritura (GET, POST, PUT)
#   - viewer: Solo lectura (GET)
#
# Columnas:
#   - role_id:     SMALLSERIAL PK, identificador unico del rol
#   - role_name:   VARCHAR(20) NOT NULL, UNIQUE, nombre del rol
#   - description: TEXT, descripcion de los permisos del rol
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   users -> User (M:N via user_roles)
#     Un rol puede ser asignado a muchos usuarios.
#     Un usuario puede tener varios roles.
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener todos los roles:
#   roles = db.query(Role).all()
#
#   # Obtener un rol con sus usuarios:
#   admin_role = db.query(Role).options(
#       selectinload(Role.users)
#   ).filter(Role.role_name == "admin").first()
#
#   # Al registrar un usuario nuevo, asignar rol "viewer":
#   viewer_role = db.query(Role).filter(Role.role_name == "viewer").first()
#   nuevo_usuario.roles.append(viewer_role)
#
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    # Relaciones
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
    )

    def __repr__(self) -> str:
        return f"<Role {self.role_id}: {self.role_name}>"
