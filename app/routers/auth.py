# app/routers/auth.py
#
# Endpoints de autenticacion y gestion de usuarios.
#
# Este router maneja el ciclo de vida completo de autenticacion:
#   - Registro de nuevos usuarios
#   - Login y generacion de tokens JWT
#   - Gestion de usuarios (admin)
#   - Asignacion de roles (admin)
#
# ============================================================================
# ENDPOINTS DE AUTENTICACION (publicos)
# ============================================================================
#
#   POST /api/auth/register
#     - Registra un nuevo usuario en el sistema.
#     - Body: RegisterRequest (username, email, password, full_name)
#     - Retorna: UserResponse (sin contrasena)
#     - Flujo:
#         1. Validar que username y email no existan.
#         2. Hashear la contrasena con bcrypt.
#         3. Crear el usuario en la BD.
#         4. Asignar rol "viewer" por defecto.
#         5. Retornar el usuario creado.
#
#   POST /api/auth/login
#     - Autentica un usuario y retorna un token JWT.
#     - Body: LoginRequest (username, password)
#     - Retorna: TokenResponse (access_token, token_type, expires_in, user)
#     - Flujo:
#         1. Buscar el usuario por username.
#         2. Verificar el hash bcrypt contra la contrasena.
#         3. Si es correcto, generar token JWT con user_id y roles.
#         4. Retornar el token y datos del usuario.
#
#   GET /api/auth/me
#     - Retorna el perfil del usuario autenticado.
#     - Requiere: Header Authorization con token JWT valido.
#     - Retorna: UserResponse con roles incluidos.
#
# ============================================================================
# ENDPOINTS DE USUARIO (requieren autenticacion)
# ============================================================================
#
#   GET /api/users
#     - Lista todos los usuarios (paginado).
#     - Requiere: Rol "admin".
#     - Retorna: UserList (items, total, page, per_page)
#
#   GET /api/users/{user_id}
#     - Obtiene un usuario por ID.
#     - Requiere: Rol "admin" o ser el mismo usuario.
#     - Retorna: UserResponse
#
#   PUT /api/users/{user_id}
#     - Actualiza datos de un usuario.
#     - Requiere: Rol "admin" o ser el mismo usuario.
#     - Body: UserUpdate (full_name, email)
#     - Retorna: UserResponse actualizado
#
#   DELETE /api/users/{user_id}
#     - Desactiva un usuario (soft delete).
#     - Requiere: Rol "admin".
#     - Retorna: 204 No Content
#
#   PUT /api/users/{user_id}/roles
#     - Asigna roles a un usuario.
#     - Requiere: Rol "admin".
#     - Body: UserUpdateRoles (role_ids: list[int])
#     - Retorna: UserResponse con roles actualizados
#
# ============================================================================
# MECANISMA DE PERMISOS
# ============================================================================
#
# Cada endpoint verifica los permisos del usuario actual:
#
#   1. El token JWT se decodifica y se extrae el user_id.
#   2. Se consultan los roles del usuario en la BD.
#   3. Se verifica si el usuario tiene el rol necesario:
#      - "admin":  Puede hacer todo (GET, POST, PUT, DELETE en todos los recursos)
#      - "user":   Puede leer y escribir (GET, POST, PUT, pero NO DELETE)
#      - "viewer": Solo puede leer (GET, pero NO POST, PUT, DELETE)
#   4. Si no tiene permiso, se retorna 403 Forbidden.
#
# ============================================================================
# FLUJO DE LOGIN COMPLETO
# ============================================================================
#
#   Cliente                          API
#     |                              |
#     |  POST /api/auth/login        |
#     |  {username, password}        |
#     |  --------------------------> |
#     |                              |  1. Buscar usuario por username
#     |                              |  2. Verificar hash bcrypt
#     |                              |  3. Generar JWT con user_id + roles
#     |  {access_token, user}        |
#     |  <--------------------------- |
#     |                              |
#     |  GET /api/customers          |
#     |  Authorization: Bearer xxx   |
#     |  --------------------------> |
#     |                              |  4. Decodificar JWT
#     |                              |  5. Obtener roles del usuario
#     |                              |  6. Verificar permiso (viewer -> GET OK)
#     |  200 OK + data               |
#     |  <--------------------------- |
#
