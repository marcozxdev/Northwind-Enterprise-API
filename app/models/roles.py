# app/models/roles.py
#
# Modelo ORM SQLAlchemy para la tabla "roles".
#
# Tabla: roles
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
# Relaciones:
#   - users: Relationship con User (muchos roles -> muchos usuarios via user_roles)
#
# Flujo de uso:
#   1. Al registrar un usuario nuevo, se le asigna el rol "viewer" por defecto.
#   2. Un admin puede cambiar el rol de cualquier usuario via PUT /api/users/{id}/roles.
#   3. Los permisos se verifican en cada endpoint usando la dependencia require_role().
#
