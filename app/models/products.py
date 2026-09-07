# models/products.py
#
# Modelo ORM SQLAlchemy para la tabla "products".
#
# Tabla: products
# Descripcion: Productos que vende la empresa Northwind.
#
# Columnas:
#   - product_id:         SMALLINT      PK, identificador unico del producto
#   - product_name:       VARCHAR(40)   NOT NULL, nombre del producto
#   - supplier_id:        SMALLINT      FK -> suppliers.supplier_id (proveedor)
#   - category_id:        SMALLINT      FK -> categories.category_id (categoria)
#   - quantity_per_unit:  VARCHAR(20)   descripcion de la unidad (ej: "10 boxes x 20 bags")
#   - unit_price:         REAL          precio unitario de venta
#   - units_in_stock:     SMALLINT      unidades disponibles en inventario
#   - units_on_order:     SMALLINT      unidades pedidas al proveedor
#   - reorder_level:      SMALLINT      nivel minimo de stock para reordenar
#   - discontinued:       INTEGER       0 = activo, 1 = descontinuado
#
# Relaciones:
#   - category:    Relationship con Category (muchos productos -> una categoria)
#   - supplier:    Relationship con Supplier (muchos productos -> un proveedor)
#   - order_details: Relationship con OrderDetail (un producto -> muchos detalles de orden)
#
