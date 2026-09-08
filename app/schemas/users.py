# app/schemas/users.py
#
# Esquemas Pydantic para el recurso Users (Usuarios) y autenticacion.
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de autenticacion y gestion de usuarios.
#
# ============================================================================
# ESQUEMAS DE AUTENTICACION
# ============================================================================
#
#   LoginRequest (POST /api/auth/login):
#     - username: str  [requerido, nombre de usuario]
#     - password: str  [requerido, contrasena en texto plano]
#
#   TokenResponse (respuesta del login):
#     - access_token: str   [token JWT generado]
#     - token_type:  str    [siempre "bearer"]
#     - expires_in:  int    [minutos hasta que expira]
#     - user:        UserResponse [datos del usuario autenticado]
#
#   RegisterRequest (POST /api/auth/register):
#     - username:  str  [requerido, min 3, max 50, unico]
#     - email:     str  [requerido, formato email, unico]
#     - password:  str  [requerido, min 6 caracteres]
#     - full_name: str  [opcional, nombre completo]
#
# ============================================================================
# ESQUEMAS DE USUARIO
# ============================================================================
#
#   UserResponse (respuesta estandar de usuario):
#     - user_id:    int
#     - username:   str
#     - email:      str
#     - full_name:  str | None
#     - is_active:  bool
#     - roles:      list[RoleResponse]
#     - created_at: datetime
#     - updated_at: datetime
#     - Config: from_attributes = True
#
#   UserUpdate (PUT /api/users/{id}):
#     - full_name: str | None  [opcional]
#     - email:     str | None  [opcional]
#     - is_active: bool | None [opcional, solo admin]
#
#   UserUpdateRoles (PUT /api/users/{id}/roles):
#     - role_ids: list[int]  [requerido, lista de role_ids a asignar]
#     - Nota: Solo un admin puede cambiar roles de otros usuarios.
#
#   UserList (respuesta paginada):
#     - items:    list[UserResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
# ============================================================================
# ESQUEMAS DE ROL
# ============================================================================
#
#   RoleResponse:
#     - role_id:     int
#     - role_name:   str
#     - description: str | None
#     - Config: from_attributes = True
#
#   RoleList:
#     - items: list[RoleResponse]
#     - total: int
#
