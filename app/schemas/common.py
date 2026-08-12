from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PagedResponse(BaseModel, Generic[T]):
    """
    Respuesta paginada estándar para cualquier lista.
    """

    items: List[T]
    total: int
    page: int
    size: int
    pages: int
