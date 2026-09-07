# app/

Directorio principal de la aplicacion FastAPI.

## Archivos

| Archivo | Descripcion |
|---|---|
| `main.py` | Punto de entrada de la API. Crea la instancia FastAPI, incluye los routers y define eventos de arranque/apagado. |
| `config.py` | Configuracion centralizada. Lee las variables de entorno desde `.env` usando `pydantic-settings`. |
| `database.py` | Configuracion de la conexion a PostgreSQL y creacion de la sesion de SQLAlchemy. |
| `dependencies.py` | Dependencias inyectables en los endpoints (ej: obtener sesion de DB, usuario autenticado, etc). |
