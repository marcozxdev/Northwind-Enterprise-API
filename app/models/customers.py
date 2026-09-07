# models/customers.py
#
# Modelo ORM SQLAlchemy para la tabla "customers".
#
# Tabla: customers
# Descripcion: Clientes de la empresa Northwind.
#
# Columnas:
#   - customer_id:   VARCHAR(5)    PK, identificador unico del cliente (ej: "ALFKI")
#   - company_name:  VARCHAR(40)   NOT NULL, nombre de la empresa
#   - contact_name:  VARCHAR(30)   nombre del contacto principal
#   - contact_title: VARCHAR(30)   cargo del contacto
#   - address:       VARCHAR(60)   direccion de la empresa
#   - city:          VARCHAR(15)   ciudad
#   - region:        VARCHAR(15)   region/estado
#   - postal_code:   VARCHAR(10)   codigo postal
#   - country:       VARCHAR(15)   pais
#   - phone:         VARCHAR(24)   telefono de contacto
#   - fax:           VARCHAR(24)   numero de fax
#
# Relaciones:
#   - orders:    Relationship con Order (un cliente tiene muchas ordenes)
#
# Convenciones:
#   - Hereda de Base (declarative_base de SQLAlchemy 2.0).
#   - __tablename__ = "customers" (nombre exacto de la tabla en la BD).
#   - Las columnas NOT NULL se definen con nullable=False.
#
