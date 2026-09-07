# schemas/customers.py
#
# Esquemas Pydantic para el recurso Customers (Clientes).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de clientes.
#
# Esquemas esperados:
#
#   CustomerCreate (request body para POST):
#     - customer_id:   str (5 caracteres, ej: "ALFKI")  [requerido]
#     - company_name:  str                               [requerido]
#     - contact_name:  str | None                        [opcional]
#     - contact_title: str | None                        [opcional]
#     - address:       str | None                        [opcional]
#     - city:          str | None                        [opcional]
#     - region:        str | None                        [opcional]
#     - postal_code:   str | None                        [opcional]
#     - country:       str | None                        [opcional]
#     - phone:         str | None                        [opcional]
#     - fax:           str | None                        [opcional]
#
#   CustomerUpdate (request body para PUT/PATCH):
#     - Todos los campos de CustomerCreate pero opcionales.
#
#   CustomerResponse (response body):
#     - Todos los campos de la tabla customers.
#     - Config: from_attributes = True (compatible con ORM).
#
#   CustomerList (respuesta paginada):
#     - items:    list[CustomerResponse]
#     - total:    int
#     - page:     int
#     - per_page: int
#
