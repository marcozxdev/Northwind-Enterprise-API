# schemas/shippers.py
#
# Esquemas Pydantic para el recurso Shippers (Transportistas).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de transportistas.
#
# Esquemas esperados:
#
#   ShipperCreate (request body para POST):
#     - company_name: str              [requerido]
#     - phone:        str | None       [opcional, telefono de contacto]
#
#   ShipperUpdate (request body para PUT/PATCH):
#     - Todos los campos de ShipperCreate pero opcionales.
#
#   ShipperResponse (response body):
#     - shipper_id:    int
#     - company_name:  str
#     - phone:         str | None
#     - Config: from_attributes = True
#
#   ShipperList:
#     - items: list[ShipperResponse]
#     - total: int
#
