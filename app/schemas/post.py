from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.user import UserSummary
from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse
from app.schemas.common import PagedResponse


class PostBase(BaseModel):
    """Campos comunes pa todos los schemas de post."""

    title: str
    content: str
    excerpt: Optional[str] = None
    status: str = "draft"  # 'draft' | 'published' | 'archived'
    published_at: Optional[datetime] = None


class PostCreate(PostBase):
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []  # IDs de tags existentes a asignar
    featured_image_id: Optional[int] = None  # <-- nuevo


class PostUpdate(PostBase):
    """
    Schema para ACTUALIZAR un post. Todos los campos son opcionales.
    """

    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    status: Optional[str] = None
    published_at: Optional[datetime] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    featured_image_id: Optional[int] = None


class PostResponse(PostBase):
    """
    Schema para RESPUESTAS. Devuelve datos del post con el autor.
    ConfigDict(from_attributes=True) permite convertir un objeto SQLAlchemy a dict.
    """

    id: int
    slug: str
    author: UserSummary
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostPagedResponse(PagedResponse[PostResponse]):
    pass
