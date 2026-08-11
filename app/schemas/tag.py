from pydantic import BaseModel, ConfigDict
from typing import Optional


class TagBase(BaseModel):
    name: str
    slug: str


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: Optional[str] = None


class TagResponse(TagBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
