# app/database.py
#
# Configuracion de la conexion a PostgreSQL con SQLAlchemy 2.0.
#
# Este archivo se encarga de:
#   1. Crear el engine de SQLAlchemy con la URL de conexion desde config.py.
#   2. Definir la clase Base para los modelos ORM (DeclarativeBase).
#   3. Crear la sessionmaker (fabrica de sesiones).
#   4. Proveer una funcion get_db() para inyectar sesiones en los endpoints.
#
# Componentes esperados:
#
#   engine:
#     - Motor de conexion a PostgreSQL via psycopg.
#     - Configurado con pool_pre_ping=True para verificar conexiones.
#
#   Base:
#     - Clase base para todos los modelos ORM.
#     - Todos los modelos heredan de esta clase.
#
#   SessionLocal:
#     - Fabrica de sesiones de BD.
#     - Una sesion por request, cerrada automaticamente al finalizar.
#
#   get_db():
#     - Generator que yield una sesion de BD.
#     - Se usa como dependencia en los endpoints:
#         @router.get("/")
#         def listar(db: Session = Depends(get_db)): ...
#
