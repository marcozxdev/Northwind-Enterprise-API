# routers/regions.py
#
# Endpoints para el recurso Regions (Regiones y Territorios).
#
# Base de datos: tablas "region", "territories" y "us_states"
#
# Endpoints esperados:
#
#   GET    /api/regions                      -> Listar todas las regiones
#   GET    /api/regions/{id}                 -> Obtener una region por region_id
#   GET    /api/regions/{id}/territories     -> Listar territorios de una region
#   POST   /api/regions                      -> Crear una nueva region
#   PUT    /api/regions/{id}                 -> Actualizar una region existente
#   DELETE /api/regions/{id}                 -> Eliminar una region
#   GET    /api/territories                  -> Listar todos los territorios
#   GET    /api/territories/{id}             -> Obtener un territorio por territory_id
#
# Esquemas Pydantic (schemas/regions.py):
#   - RegionCreate:      Body para POST
#   - RegionUpdate:      Body para PUT (campos opcionales)
#   - RegionResponse:    Respuesta estandarizada
#   - TerritoryResponse: Respuesta de territorios
#   - RegionList:        Lista de regiones
#
# Modelo ORM (models/regions.py):
#   - Region:     modelo que mapea la tabla "region"
#   - Territory:  modelo que mapea la tabla "territories"
#   - UsState:    modelo que mapea la tabla "us_states"
#
