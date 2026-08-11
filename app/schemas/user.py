from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Campos comunes pa todos los schemas de usuario."""

    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema para REGISTRO. Incluye password porque el usuario lo envía.
    NUNCA devolvemos la password en una respuesta.
    """

    password: str


class UserResponse(UserBase):
    """
    Schema para RESPUESTAS. Devuelve datos del usuario SIN password.
    ConfigDict(from_attributes=True) permite convertir un objeto SQLAlchemy a dict.
    """

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema para el token JWT."""

    access_token: str
    token_type: str = "bearer"
    
    
class TokenPayload(BaseModel):
    """Schema para el payload del token JWT."""

    sub: Optional[str] = None
    
    
class UserSummary(UserBase):
    """Schema para mostrar un resumen del usuario."""

    id: int
    username: str
    full_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)