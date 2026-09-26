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
# ============================================================================
# USO
# ============================================================================
#
#   from app.database import Base, engine, get_db
#
#   # Para crear todas las tablas (solo en desarrollo/migraciones):
#   Base.metadata.create_all(bind=engine)
#
#   # En un endpoint:
#   @router.get("/")
#   def listar(db: Session = Depends(get_db)):
#       resultados = db.query(SomeModel).all()
#       return resultados
#
# ============================================================================
# FLUJO DE CONEXION
# ============================================================================
#
#   1. settings.db.DATABASE_URL se lee desde .env
#   2. Se crea el engine con pool_pre_ping (verifica conexiones muertas)
#   3. Cada request obtiene una sesion via get_db()
#   4. La sesion se cierra automaticamente al finalizar el request
#

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Engine de conexion a PostgreSQL
# pool_pre_ping=True: antes de usar una conexion, verifica que este viva
engine = create_engine(
    settings.db.DATABASE_URL,
    pool_pre_ping=True,
)

# Fabrica de sesiones
# autocommit=False: las transacciones se confirman manualmente
# autoflush=False: los cambios no se envian a la BD hasta hacer commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Clase base para todos los modelos ORM
# Todos los modelos heredan de esta clase
# Ejemplo: class MiModelo(Base): __tablename__ = "mi_tabla"
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependencia para inyectar sesiones de BD en los endpoints.

    Uso en un endpoint:
        @router.get("/")
        def listar(db: Session = Depends(get_db)):
            return db.query(Model).all()

    La sesion se crea al inicio del request y se cierra automaticamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
