from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Esta clase lee automáticamente las variables del archivo .env.
    Pydantic las valida y convierte al tipo correcto.
    """

    PROJECT_NAME: str = "CMS API"
    DEBUG: bool = False

    # Base de datos
    DATABASE_URL: str

    # Seguridad (JWT)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Función para obtener la configuración de la aplicación.
    Se utiliza lru_cache para que la configuración se cargue una sola vez y se reutilice.
    """
    return Settings()


# Exportamos una instancia para usarla fácilmente
settings = get_settings()
