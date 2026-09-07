# app/dependencies.py
#
# Dependencias inyectables para los endpoints de FastAPI.
#
# FastAPI permite inyectar dependencias en los parametros de los endpoints
# usando Depends(). Este archivo centraliza esas dependencias comunes.
#
# Dependencias esperadas:
#
#   get_db():
#     - Obtiene una sesion de BD y la cierra al finalizar el request.
#     - Ya definida en database.py, re-exportada aqui si es necesario.
#
#   get_current_user(token: str = Depends(oauth2_scheme)):
#     - Valida el token JWT del header Authorization.
#     - Decodifica el payload y retorna el usuario actual.
#     - Lanza HTTPException(401) si el token es invalido o expiro.
#
#   get_current_active_user(current_user = Depends(get_current_user)):
#     - Verifica que el usuario este activo (no deshabilitado).
#     - Lanza HTTPException(403) si el usuario esta inactivo.
#
#   require_role(role: str):
#     - Factory que retorna una dependencia que verifica el rol del usuario.
#     - Ej: admin_only = require_role("admin")
#     - Lanza HTTPException(403) si el usuario no tiene el rol requerido.
#
# Ejemplo de uso en un endpoint:
#
#   @router.get("/me")
#   def perfil_usuario(current_user = Depends(get_current_active_user)):
#       return current_user
#
