# database/seed.py
#
# Script para poblar la base de datos con datos de prueba.
#
# Este script se ejecuta una vez despues de levantar la BD para crear:
#   1. Roles por defecto (admin, user, viewer)
#   2. Usuario administrador inicial
#   3. Datos de ejemplo (opcional, en desarrollo)
#
# ============================================================================
# USO
# ============================================================================
#
#   # Ejecutar desde la raiz del proyecto:
#   python -m database.seed
#
#   # O desde Docker:
#   docker-compose exec api python -m database.seed
#
# ============================================================================
# REQUISITOS
# ============================================================================
#
#   - La BD debe estar corriendo (docker-compose up -d)
#   - Las tablas deben estar creadas (init.sql ejecutado)
#   - Paquetes: psycopg, bcrypt, python-dotenv
#
# ============================================================================
# FLUJO
# ============================================================================
#
#   1. Lee las variables de entorno desde .env
#   2. Conecta a PostgreSQL
#   3. Verifica si ya existen roles y usuarios
#   4. Si no existen, crea:
#      - Roles: admin (1), user (2), viewer (3)
#      - Usuario admin: admin / admin123
#   5. Asigna el rol "admin" al usuario admin
#   6. Imprime un resumen de lo creado
#
# ============================================================================
# CREDENCIALES DEL ADMIN POR DEFECTO
# ============================================================================
#
#   Username: admin
#   Password: admin123
#   Email:    admin@northwind.com
#
#   IMPORTANTE: Cambia la contrasena en produccion!
#
