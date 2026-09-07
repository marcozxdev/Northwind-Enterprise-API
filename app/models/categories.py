# models/categories.py
#
# Modelo ORM SQLAlchemy para la tabla "categories".
#
# Tabla: categories
# Descripcion: Categorias de productos (ej: Beverages, Condiments, Seafood).
#
# Columnas:
#   - category_id:    SMALLINT      PK, identificador unico de la categoria
#   - category_name:  VARCHAR(15)   NOT NULL, nombre de la categoria
#   - description:    TEXT          descripcion de la categoria
#   - picture:        BYTEA         imagen de la categoria (bytes)
#
# Relaciones:
#   - products:  Relationship con Product (una categoria -> muchos productos)
#
# Notas:
#   - Solo hay 8 categorias en la BD Northwind.
#
