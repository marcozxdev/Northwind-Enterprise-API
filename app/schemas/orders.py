# schemas/orders.py
#
# Esquemas Pydantic para el recurso Orders (Ordenes de compra).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de ordenes y sus detalles.
#
# Esquemas esperados:
#
#   OrderCreate (request body para POST):
#     - customer_id:   str | None       [opcional, cliente que hizo la orden]
#     - employee_id:   int | None       [opcional, empleado que tomo la orden]
#     - order_date:    date | None      [opcional, fecha de la orden]
#     - required_date: date | None      [opcional, fecha requerida de entrega]
#     - shipped_date:  date | None      [opcional, fecha de envio]
#     - ship_via:      int | None       [opcional, transportista]
#     - freight:       float | None     [opcional, costo de flete]
#     - ship_name:     str | None       [opcional, nombre para envio]
#     - ship_address:  str | None       [opcional, direccion de envio]
#     - ship_city:     str | None       [opcional, ciudad de envio]
#     - ship_region:   str | None       [opcional, region de envio]
#     - ship_postal_code: str | None    [opcional, codigo postal de envio]
#     - ship_country:  str | None       [opcional, pais de envio]
#     - details:       list[OrderDetailCreate] [opcional, detalles de la orden]
#
#   OrderDetailCreate:
#     - product_id:  int    [requerido]
#     - unit_price:  float  [requerido]
#     - quantity:    int    [requerido]
#     - discount:    float  [requerido, default 0]
#
#   OrderUpdate (request body para PUT/PATCH):
#     - Todos los campos de OrderCreate pero opcionales.
#
#   OrderResponse (response body):
#     - Todos los campos de la tabla orders.
#     - Incluye detalles: list[OrderDetailResponse]
#     - Config: from_attributes = True
#
#   OrderDetailResponse:
#     - order_id, product_id, unit_price, quantity, discount
#
#   OrderList (respuesta paginada):
#     - items:    list[OrderResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
