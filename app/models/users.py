# app/models/users.py
#
# Modelos ORM SQLAlchemy para las tablas "users" y "user_roles".
#
# ============================================================================
# TABLA: users
# ============================================================================
# Descripcion: Usuarios del sistema de autenticacion.
#
# Cada usuario tiene credenciales para acceder a la API.
# Las contrasenas NUNCA se almacenan en texto plano, solo el hash bcrypt.
#
# Columnas:
#   - user_id:         SERIAL PK, identificador unico del usuario
#   - username:        VARCHAR(50) NOT NULL, UNIQUE, nombre de usuario para login
#   - email:           VARCHAR(100) NOT NULL, UNIQUE, correo electronico
#   - hashed_password: VARCHAR(255) NOT NULL, hash bcrypt de la contrasena
#   - full_name:       VARCHAR(100), nombre completo del usuario
#   - is_active:       BOOLEAN DEFAULT true, si la cuenta esta activa
#   - created_at:      TIMESTAMP DEFAULT NOW(), fecha de creacion
#   - updated_at:      TIMESTAMP DEFAULT NOW(), fecha de ultima actualizacion
#
# ============================================================================
# TABLA: user_roles
# ============================================================================
# Descripcion: Tabla asociativa entre users y roles.
#
# Columnas:
#   - user_id: INT PK, FK -> users.user_id (ON DELETE CASCADE)
#   - role_id: SMALLINT PK, FK -> roles.role_id (ON DELETE CASCADE)
#
# ============================================================================
# RELACIONES
# ============================================================================
#
#   roles -> Role (M:N via user_roles)
#     Un usuario puede tener varios roles (ej: admin + user).
#     Un rol puede ser asignado a muchos usuarios.
#
# ============================================================================
# FLUJO DE AUTENTICACION
# ============================================================================
#
#   1. El usuario envia POST /api/auth/login con username + password.
#   2. El sistema verifica el hash bcrypt contra la contrasena enviada.
#   3. Si es correcto, genera un token JWT con el user_id y sus roles.
#   4. El token se envia en el header Authorization: Bearer <token>.
#   5. En cada request, se decodifica el token y se verifican los permisos.
#
# ============================================================================
# FLUJO DE REGISTRO
# ============================================================================
#
#   1. El usuario envia POST /api/auth/register con username, email, password.
#   2. Se hashea la contrasena con bcrypt.
#   3. Se crea el usuario con is_active=True.
#   4. Se asigna el rol "viewer" por defecto.
#   5. Se retorna el usuario creado (sin la contrasena).
#
# ============================================================================
# FLUJO DE USO
# ============================================================================
#
#   # Obtener un usuario con sus roles:
#   usuario = db.query(User).options(
#       selectinload(User.roles)
#   ).filter(User.username == "admin").first()
#   # usuario.roles = [Role(role_name="admin")]
#
#   # Asignar un rol a un usuario:
#   admin_role = db.query(Role).filter(Role.role_name == "admin").first()
#   usuario.roles.append(admin_role)
#   db.commit()
#
#   # Verificar si un usuario tiene un rol:
#   tiene_admin = any(r.role_name == "admin" for r in usuario.roles)
#
from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# Tabla asociativa user_roles
# Define la relacion M:N entre users y roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
    )

    @property
    def role_names(self) -> list[str]:
        """Retorna una lista con los nombres de los roles del usuario."""
        return [role.role_name for role in self.roles]

    def has_role(self, role_name: str) -> bool:
        """Verifica si el usuario tiene un rol especifico."""
        return role_name in self.role_names

    def __repr__(self) -> str:
        return f"<User {self.user_id}: {self.username}>"
