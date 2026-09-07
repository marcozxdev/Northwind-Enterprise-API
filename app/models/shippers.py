# models/shippers.py
#
# Modelo ORM SQLAlchemy para la tabla "shippers".
#
# Tabla: shippers
# Descripcion: Transportistas que envian los pedidos (ej: Speedy Express, United Package).
#
# Columnas:
#   - shipper_id:    SMALLINT      PK, identificador unico del transportista
#   - company_name:  VARCHAR(40)   NOT NULL, nombre de la empresa de envios
#   - phone:         VARCHAR(24)   telefono de contacto
#
# Relaciones:
#   - orders:  Relationship con Order (un transportista -> muchas ordenes)
#
# Notas:
#   - Solo hay 3 transportistas en la BD Northwind.
#
