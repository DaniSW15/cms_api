from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_ 
from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Optional[Post]:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_by_slug(self, slug: str) -> Optional[Post]:
        return self.db.query(Post).filter(Post.slug == slug).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.db.query(Post).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> Post:
        db_obj = Post(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Post, obj_in: dict) -> Post:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Post) -> None:
        self.db.delete(db_obj)
        self.db.commit()

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        search: str = None,
        status: str = None,
        category_id: int = None,
        tag_ids: list = None,
        author_id: int = None,
    ):
        """
        Búsqueda y filtros dinámicos. Solo aplica filtros si se envían.
        """
        query = self.db.query(Post)

        # Filtro por texto (busca en título y contenido)
        if search:
            search_filter = or_(
                Post.title.ilike(f"%{search}%"), Post.content.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)

        # Filtro por status
        if status:
            query = query.filter(Post.status == status)

        # Filtro por categoría
        if category_id:
            query = query.filter(Post.category_id == category_id)

        # Filtro por autor
        if author_id:
            query = query.filter(Post.author_id == author_id)

        # Filtro por tags (mucho más avanzado, lo simplificamos)
        # Para filtrar por tags necesitamos un join, lo dejamos para más adelante
        # o puedes agregarlo como bonus

        # Contar total antes de paginar
        total = query.count()

        # Aplicar paginación
        items = query.offset(skip).limit(limit).all()

        return items, total
