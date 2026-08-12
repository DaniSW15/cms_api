from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.user import UserSummary


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    """Lo que envías para crear un comentario."""

    pass


class CommentUpdate(BaseModel):
    """Lo que envías para editar un comentario."""

    content: str


class CommentResponse(CommentBase):
    """Lo que devuelve la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    author: UserSummary
    created_at: datetime
    updated_at: datetime
