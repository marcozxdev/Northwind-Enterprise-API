# app/repositories/users.py
#
# Repository para el modelo User.
#
# Este repository encapsula todas las consultas SQL relacionadas
# con la tabla users y la tabla asociativa user_roles.
#
# ============================================================================
# METODOS ESPECIFICOS
# ============================================================================
#
#   get_by_username(username):
#     - Busca un usuario por su nombre de usuario
#     - Carga eagermente los roles
#
#   get_by_email(email):
#     - Busca un usuario por su email
#
#   get_with_roles(user_id):
#     - Obtiene un usuario con sus roles cargados
#
#   get_all_with_roles(page, per_page):
#     - Lista todos los usuarios con sus roles (paginado)
#
#   create_with_roles(data, role_ids):
#     - Crea un usuario y le asigna roles
#
#   update_roles(user_id, role_ids):
#     - Reemplaza los roles de un usuario
#
#   search(query, page, per_page):
#     - Busca usuarios por username o email
#

from sqlalchemy.orm import Session, selectinload

from app.models.roles import Role
from app.models.users import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository para el modelo User.

    Hereda de BaseRepository:
        - get_by_id()
        - get_all()
        - create()
        - update()
        - delete()
        - count()
    """

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> User | None:
        """
        Obtiene un usuario por su nombre de usuario.

        Args:
            username: Nombre de usuario (ej: "admin")

        Returns:
            User | None: Usuario encontrado o None
        """
        return self.db.query(User).options(
            selectinload(User.roles)
        ).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User | None:
        """
        Obtiene un usuario por su email.

        Args:
            email: Correo electronico

        Returns:
            User | None: Usuario encontrado o None
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_with_roles(self, user_id: int) -> User | None:
        """
        Obtiene un usuario con sus roles cargados.

        Args:
            user_id: ID del usuario

        Returns:
            User | None: Usuario con roles o None
        """
        return self.db.query(User).options(
            selectinload(User.roles)
        ).filter(User.user_id == user_id).first()

    def get_all_with_roles(self, page: int = 1, per_page: int = 10) -> tuple[list[User], int]:
        """
        Obtiene todos los usuarios con sus roles (paginado).

        Returns:
            tuple: (lista de usuarios con roles, total)
        """
        query = self.db.query(User).options(selectinload(User.roles))
        total = self.db.query(User).count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        return items, total

    def create_with_roles(self, data: dict, role_ids: list[int]) -> User:
        """
        Crea un usuario y le asigna roles.

        Args:
            data: Diccionario con campos del usuario
            role_ids: Lista de role_ids a asignar

        Returns:
            User: Usuario creado con roles
        """
        db_user = User(**data)
        self.db.add(db_user)
        self.db.flush()

        if role_ids:
            roles = self.db.query(Role).filter(Role.role_id.in_(role_ids)).all()
            db_user.roles = roles

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_roles(self, user_id: int, role_ids: list[int]) -> User | None:
        """
        Reemplaza los roles de un usuario.

        Args:
            user_id: ID del usuario
            role_ids: Nuevos role_ids

        Returns:
            User | None: Usuario con roles actualizados
        """
        user = self.get_with_roles(user_id)
        if not user:
            return None

        new_roles = self.db.query(Role).filter(Role.role_id.in_(role_ids)).all()
        user.roles = new_roles

        self.db.commit()
        self.db.refresh(user)
        return user

    def search(self, query: str, page: int = 1, per_page: int = 10) -> tuple[list[User], int]:
        """
        Busca usuarios por username o email.

        Args:
            query: Texto a buscar
            page: Pagina
            per_page: Registros por pagina

        Returns:
            tuple: (lista de usuarios, total)
        """
        search = f"%{query}%"
        query_obj = self.db.query(User).options(
            selectinload(User.roles)
        ).filter(
            (User.username.ilike(search)) | (User.email.ilike(search))
        )

        total = query_obj.count()
        items = query_obj.offset((page - 1) * per_page).limit(per_page).all()
        return items, total
