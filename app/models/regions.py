# models/regions.py
#
# Modelos ORM SQLAlchemy para las tablas "region", "territories" y "us_states".
#
# Tabla: region
# Descripcion: Regiones geograficas (ej: Eastern, Western, Northern, Southern).
#
# Columnas de region:
#   - region_id:            SMALLINT      PK, identificador unico de la region
#   - region_description:   VARCHAR(60)   NOT NULL, descripcion de la region
#
# Relaciones de region:
#   - territories:  Relationship con Territory (una region -> muchos territorios)
#
# Tabla: territories
# Descripcion: Territorios especificos dentro de cada region.
#
# Columnas de territories:
#   - territory_id:            VARCHAR(20)  PK, identificador del territorio
#   - territory_description:   VARCHAR(60)  NOT NULL, descripcion del territorio
#   - region_id:               SMALLINT     FK -> region.region_id
#
# Relaciones de territories:
#   - region:     Relationship con Region (un territorio -> una region)
#   - employees:  Relationship con Employee (via employee_territories)
#
# Tabla: us_states
# Descripcion: Estados de Estados Unidos (para referencia geografica).
#
# Columnas de us_states:
#   - state_id:      SMALLINT      PK, identificador del estado
#   - state_name:    VARCHAR(100)  nombre del estado
#   - state_abbr:    VARCHAR(2)    abreviatura (ej: "WA", "CA")
#   - state_region:  VARCHAR(50)   region del estado
#
