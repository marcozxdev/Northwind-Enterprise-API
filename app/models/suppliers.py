# models/suppliers.py
#
# Modelo ORM SQLAlchemy para la tabla "suppliers".
#
# Tabla: suppliers
# Descripcion: Proveedores de productos para Northwind.
#
# Columnas:
#   - supplier_id:    SMALLINT      PK, identificador unico del proveedor
#   - company_name:   VARCHAR(40)   NOT NULL, nombre de la empresa proveedora
#   - contact_name:   VARCHAR(30)   nombre del contacto
#   - contact_title:  VARCHAR(30)   cargo del contacto
#   - address:        VARCHAR(60)   direccion de la empresa
#   - city:           VARCHAR(15)   ciudad
#   - region:         VARCHAR(15)   region/estado
#   - postal_code:    VARCHAR(10)   codigo postal
#   - country:        VARCHAR(15)   pais
#   - phone:          VARCHAR(24)   telefono de contacto
#   - fax:            VARCHAR(24)   numero de fax
#   - homepage:       TEXT          URL del sitio web del proveedor
#
# Relaciones:
#   - products:  Relationship con Product (un proveedor -> muchos productos)
#
