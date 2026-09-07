# schemas/suppliers.py
#
# Esquemas Pydantic para el recurso Suppliers (Proveedores).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de proveedores.
#
# Esquemas esperados:
#
#   SupplierCreate (request body para POST):
#     - company_name:  str              [requerido]
#     - contact_name:  str | None       [opcional, nombre del contacto]
#     - contact_title: str | None       [opcional, cargo del contacto]
#     - address:       str | None       [opcional, direccion]
#     - city:          str | None       [opcional, ciudad]
#     - region:        str | None       [opcional, region]
#     - postal_code:   str | None       [opcional, codigo postal]
#     - country:       str | None       [opcional, pais]
#     - phone:         str | None       [opcional, telefono]
#     - fax:           str | None       [opcional, fax]
#     - homepage:      str | None       [opcional, URL del sitio web]
#
#   SupplierUpdate (request body para PUT/PATCH):
#     - Todos los campos de SupplierCreate pero opcionales.
#
#   SupplierResponse (response body):
#     - Todos los campos de la tabla suppliers.
#     - Config: from_attributes = True
#
#   SupplierList (respuesta paginada):
#     - items:    list[SupplierResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
