# app/schemas/customers.py
#
# Esquemas Pydantic para el recurso Customers (Clientes).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de clientes.
#
# ============================================================================
# ESQUEMAS
# ============================================================================
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

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    """
    Cuerpo del request para POST /api/customers

    Campos:
        - customer_id:   str [requerido, 5 caracteres]
        - company_name:  str [requerido, max 40]
        - contact_name:  str | None [opcional]
        - contact_title: str | None [opcional]
        - address:       str | None [opcional]
        - city:          str | None [opcional]
        - region:        str | None [opcional]
        - postal_code:   str | None [opcional]
        - country:       str | None [opcional]
        - phone:         str | None [opcional]
        - fax:           str | None [opcional]
    """
    customer_id: str = Field(..., min_length=5, max_length=5)
    company_name: str = Field(..., min_length=1, max_length=40)
    contact_name: str | None = Field(None, max_length=30)
    contact_title: str | None = Field(None, max_length=30)
    address: str | None = Field(None, max_length=60)
    city: str | None = Field(None, max_length=15)
    region: str | None = Field(None, max_length=15)
    postal_code: str | None = Field(None, max_length=10)
    country: str | None = Field(None, max_length=15)
    phone: str | None = Field(None, max_length=24)
    fax: str | None = Field(None, max_length=24)


class CustomerUpdate(BaseModel):
    """
    Cuerpo del request para PUT /api/customers/{customer_id}
    Todos los campos son opcionales (solo se actualizan los enviados).
    """
    company_name: str | None = Field(None, max_length=40)
    contact_name: str | None = Field(None, max_length=30)
    contact_title: str | None = Field(None, max_length=30)
    address: str | None = Field(None, max_length=60)
    city: str | None = Field(None, max_length=15)
    region: str | None = Field(None, max_length=15)
    postal_code: str | None = Field(None, max_length=10)
    country: str | None = Field(None, max_length=15)
    phone: str | None = Field(None, max_length=24)
    fax: str | None = Field(None, max_length=24)


class CustomerResponse(BaseModel):
    """
    Respuesta estandar de un cliente.

    Config:
        - from_attributes = True
    """
    customer_id: str
    company_name: str
    contact_name: str | None
    contact_title: str | None
    address: str | None
    city: str | None
    region: str | None
    postal_code: str | None
    country: str | None
    phone: str | None
    fax: str | None

    model_config = {"from_attributes": True}


class CustomerList(BaseModel):
    """Respuesta paginada de clientes."""
    items: list[CustomerResponse]
    total: int
    page: int
    per_page: int
