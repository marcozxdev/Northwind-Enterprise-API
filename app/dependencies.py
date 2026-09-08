# app/dependencies.py
#
# Dependencias inyectables para los endpoints de FastAPI.
#
# FastAPI permite inyectar dependencias en los parametros de los endpoints
# usando Depend(). Este archivo centraliza las dependencias comunes,
# especialmente las de autenticacion y autorizacion.
#
# ============================================================================
# FLUJO DE AUTENTICACION
# ============================================================================
#
#   1. El cliente envia un request con header: Authorization: Bearer <token>
#   2. OAuth2PasswordBearer extrae el token del header.
#   3. get_current_user() decodifica el JWT y retorna el usuario.
#   4. get_current_active_user() verifica que el usuario este activo.
#   5. require_role("admin") verifica que el usuario tenga el rol necesario.
#
# ============================================================================
# DEPENDENCIAS
# ============================================================================
#
#   get_db():
#     - Obtiene una sesion de BD y la cierra al finalizar el request.
#     - Se usa en cada endpoint que necesite acceder a la BD.
#     - Ej: def listar(db: Session = Depends(get_db)): ...
#
#   oauth2_scheme:
#     - Instancia de OAuth2PasswordBearer que apunta a /api/auth/login.
#     - Extrae el token del header Authorization automaticamente.
#     - Si no hay token, retorna None (no lanza error aun).
#
#   get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
#     - Decodifica el token JWT usando la clave secreta.
#     - Busca el usuario en la BD por el user_id del token.
#     - Retorna el objeto User de la BD.
#     - Lanza HTTPException(401) si:
#         * El token es invalido o esta corrupto.
#         * El token ha expirado.
#         * El usuario no existe en la BD.
#
#   get_current_active_user(current_user = Depends(get_current_user)):
#     - Verifica que el campo is_active del usuario sea True.
#     - Lanza HTTPException(403) si el usuario esta desactivado.
#     - Se usa para proteger endpoints que requieren una cuenta activa.
#
#   require_role(roles: list[str]):
#     - Factory que retorna una dependencia que verifica el rol del usuario.
#     - Recibe una lista de roles permitidos.
#     - Consulta los roles del usuario actual en la BD (via user_roles).
#     - Lanza HTTPException(403) si el usuario no tiene ninguno de los roles.
#     - Uso comun:
#         admin_only = require_role(["admin"])
#         admin_or_user = require_role(["admin", "user"])
#
# ============================================================================
# EJEMPLO DE USO EN UN ENDPOINT
# ============================================================================
#
#   from fastapi import Depends
#   from app.dependencies import get_db, get_current_active_user, require_role
#   from app.models.users import User
#
#   # Endpoint publico (solo necesita estar autenticado)
#   @router.get("/me")
#   def perfil_usuario(current_user: User = Depends(get_current_active_user)):
#       return current_user
#
#   # Endpoint solo para admin
#   @router.delete("/users/{user_id}")
#   def eliminar_usuario(
#       user_id: int,
#       db: Session = Depends(get_db),
#       current_user: User = Depends(require_role(["admin"]))
#   ):
#       ...
#
#   # Endpoint para admin o el mismo usuario
#   @router.put("/users/{user_id}")
#   def actualizar_usuario(
#       user_id: int,
#       data: UserUpdate,
#       db: Session = Depends(get_db),
#       current_user: User = Depends(require_role(["admin", "user"]))
#   ):
#       ...
#
