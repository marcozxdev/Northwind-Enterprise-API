# schemas/regions.py
#
# Esquemas Pydantic para el recurso Regions (Regiones y Territorios).
#
# Estos esquemas definen la estructura de los datos que se reciben
# y se envian en los endpoints de regiones y territorios.
#
# Esquemas esperados:
#
#   RegionCreate (request body para POST):
#     - region_description: str  [requerido, max 60 caracteres]
#
#   RegionUpdate (request body para PUT/PATCH):
#     - region_description: str | None  [opcional]
#
#   RegionResponse (response body):
#     - region_id:          int
#     - region_description: str
#     - Config: from_attributes = True
#
#   TerritoryResponse:
#     - territory_id:          str
#     - territory_description: str
#     - region_id:             int
#     - region_name:           str | None (join con region)
#
#   RegionList:
#     - items: list[RegionResponse]
#     - total: int
#
