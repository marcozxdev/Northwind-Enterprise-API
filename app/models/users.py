# app/models/users.py
#
# Modelos ORM SQLAlchemy para las tablas "users" y "user_roles".
#
# Tabla: users
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
# Relaciones:
#   - roles: Relationship con Role (via user_roles, muchos a muchos)
#
# Tabla: user_roles
# Descripcion: Tabla asociativa entre users y roles.
#
# Columnas:
#   - user_id: INT PK, FK -> users.user_id (ON DELETE CASCADE)
#   - role_id: SMALLINT PK, FK -> roles.role_id (ON DELETE CASCADE)
#
# Flujo de autenticacion:
#   1. El usuario envia POST /api/auth/login con username + password.
#   2. El sistema verifica el hash bcrypt contra la contrasena enviada.
#   3. Si es correcto, genera un token JWT con el user_id y sus roles.
#   4. El token se envia en el header Authorization: Bearer <token>.
#   5. En cada request, se decodifica el token y se verifican los permisos.
#
# Flujo de registro:
#   1. El usuario envia POST /api/auth/register con username, email, password.
#   2. Se hashea la contrasena con bcrypt.
#   3. Se crea el usuario con is_active=True.
#   4. Se asigna el rol "viewer" por defecto.
#   5. Se retorna el usuario creado (sin la contrasena).
#
