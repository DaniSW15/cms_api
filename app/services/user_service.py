from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_create: UserCreate):
        # Verificar si el email o username ya existe
        if self.user_repo.get_by_email(user_create.email):
            raise ValueError("El email ya está en uso.")
        if self.user_repo.get_by_username(user_create.username):
            raise ValueError("El nombre de usuario ya está en uso.")

        # Convertimos el schema a dict, sacamos la password plana y la reemplazamos por su hash
        user_data = user_create.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

        return self.user_repo.create(user_data)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """Verifica email + password. Devuelve el usuario si es correcto, None si no."""
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user