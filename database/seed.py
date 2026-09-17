# database/seed.py
#
# Script para poblar la base de datos con datos iniciales.
#
# Este script se ejecuta una vez despues de levantar la BD para crear:
#   1. Roles por defecto (admin, user, viewer)
#   2. Usuario administrador inicial
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
# CREDENCIALES DEL ADMIN POR DEFECTO
# ============================================================================
#
#   Username: admin
#   Password: admin123
#   Email:    admin@northwind.com
#
#   IMPORTANTE: Cambia la contrasena en produccion!
#
import os
import sys

# Agregar el directorio raiz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.roles import Role
from app.models.users import User


def seed_roles(db):
    """
    Crea los roles por defecto si no existen.

    Roles:
        1. admin  - Acceso completo CRUD
        2. user   - Lectura y escritura
        3. viewer - Solo lectura
    """
    roles_to_create = [
        {"role_name": "admin", "description": "Acceso completo a todos los recursos"},
        {"role_name": "user", "description": "Lectura y escritura (sin DELETE)"},
        {"role_name": "viewer", "description": "Solo lectura (GET)"},
    ]

    created = 0
    for role_data in roles_to_create:
        existing = db.query(Role).filter(Role.role_name == role_data["role_name"]).first()
        if not existing:
            role = Role(**role_data)
            db.add(role)
            created += 1

    db.commit()
    return created


def seed_admin_user(db):
    """
    Crea el usuario administrador por defecto si no existe.
    """
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        return False

    admin_role = db.query(Role).filter(Role.role_name == "admin").first()
    if not admin_role:
        print("Error: El rol 'admin' no existe. Ejecuta seed_roles primero.")
        return False

    admin_user = User(
        username="admin",
        email="admin@northwind.com",
        hashed_password=hash_password("admin123"),
        full_name="Administrador",
        is_active=True,
    )
    admin_user.roles.append(admin_role)

    db.add(admin_user)
    db.commit()
    return True


def run_seed():
    """Ejecuta el seed completo."""
    db = SessionLocal()

    try:
        print("Iniciando seed de la base de datos...")

        roles_created = seed_roles(db)
        print(f"Roles: {roles_created} creados")

        admin_created = seed_admin_user(db)
        if admin_created:
            print("Usuario admin creado: admin / admin123")
        else:
            print("Usuario admin ya existe")

        print("Seed completado exitosamente!")

    except Exception as e:
        print(f"Error durante el seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
