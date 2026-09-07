# models/orders.py
#
# Modelos ORM SQLAlchemy para las tablas "orders" y "order_details".
#
# Tabla: orders
# Descripcion: Ordenes de compra realizadas por los clientes.
#
# Columnas de orders:
#   - order_id:          SMALLINT    PK, identificador unico de la orden
#   - customer_id:       VARCHAR(5)  FK -> customers.customer_id
#   - employee_id:       SMALLINT    FK -> employees.employee_id
#   - order_date:        DATE        fecha en que se registro la orden
#   - required_date:     DATE        fecha en que se requiere la entrega
#   - shipped_date:      DATE        fecha en que se envio
#   - ship_via:          SMALLINT    FK -> shippers.shipper_id (transportista)
#   - freight:           REAL        costo total del flete
#   - ship_name:         VARCHAR(40) nombre para el envio
#   - ship_address:      VARCHAR(60) direccion de envio
#   - ship_city:         VARCHAR(15) ciudad de envio
#   - ship_region:       VARCHAR(15) region de envio
#   - ship_postal_code:  VARCHAR(10) codigo postal de envio
#   - ship_country:      VARCHAR(15) pais de envio
#
# Relaciones de orders:
#   - customer:    Relationship con Customer
#   - employee:    Relationship con Employee
#   - shipper:     Relationship con Shipper (via ship_via)
#   - details:     Relationship con OrderDetail (una orden tiene muchos detalles)
#
# Tabla: order_details
# Descripcion: Detalles (line items) de cada orden.
#
# Columnas de order_details:
#   - order_id:    SMALLINT  PK, FK -> orders.order_id
#   - product_id:  SMALLINT  PK, FK -> products.product_id
#   - unit_price:  REAL      precio unitario al momento de la compra
#   - quantity:    SMALLINT  cantidad ordenada
#   - discount:    REAL      descuento aplicado (0 a 1)
#
# Relaciones de order_details:
#   - order:   Relationship con Order
#   - product: Relationship con Product
#
