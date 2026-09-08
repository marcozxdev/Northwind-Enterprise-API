# app/routers/users.py
#
# Endpoints de gestion de usuarios (solo administradores).
#
# Este router maneja las operaciones CRUD de usuarios.
# Todos los endpoints requieren autenticacion y rol "admin".
#
# ============================================================================
# ENDPOINTS
# ============================================================================
#
#   GET /api/users
#     - Lista todos los usuarios (paginado).
#     - Requiere: Rol "admin".
#     - Query params: page, per_page, search (buscar por username o email)
#     - Retorna: UserList (items, total, page, per_page)
#     - Flujo:
#         1. Verificar que el usuario actual tenga rol "admin".
#         2. Consultar la tabla users con paginacion.
#         3. Para cada usuario, consultar sus roles via user_roles.
#         4. Retornar la lista sin incluir hashed_password.
#
#   GET /api/users/{user_id}
#     - Obtiene un usuario por ID.
#     - Requiere: Rol "admin" o ser el mismo usuario.
#     - Retorna: UserResponse con roles incluidos.
#     - Flujo:
#         1. Verificar permisos (admin o self).
#         2. Buscar usuario por user_id.
#         3. Consultar roles del usuario.
#         4. Retornar usuario sin hashed_password.
#
#   PUT /api/users/{user_id}
#     - Actualiza datos de un usuario.
#     - Requiere: Rol "admin" o ser el mismo usuario.
#     - Body: UserUpdate (full_name, email)
#     - Retorna: UserResponse actualizado.
#     - Flujo:
#         1. Verificar permisos (admin o self).
#         2. Verificar que el email no este en uso por otro usuario.
#         3. Actualizar los campos proporcionados.
#         4. Actualizar updated_at.
#         5. Retornar el usuario actualizado.
#
#   DELETE /api/users/{user_id}
#     - Desactiva un usuario (soft delete, no elimina de la BD).
#     - Requiere: Rol "admin".
#     - Retorna: 204 No Content.
#     - Flujo:
#         1. Verificar que el usuario actual sea admin.
#         2. No permitir que el admin se desactive a si mismo.
#         3. Cambiar is_active a False.
#         4. Retornar 204.
#
#   PUT /api/users/{user_id}/roles
#     - Asigna roles a un usuario (reemplaza los existentes).
#     - Requiere: Rol "admin".
#     - Body: UserUpdateRoles (role_ids: list[int])
#     - Retorna: UserResponse con roles actualizados.
#     - Flujo:
#         1. Verificar que el usuario actual sea admin.
#         2. Verificar que todos los role_ids existan en la tabla roles.
#         3. Eliminar los roles actuales del usuario (DELETE user_roles).
#         4. Insertar los nuevos roles (INSERT user_roles).
#         5. Retornar el usuario con los roles actualizados.
#
