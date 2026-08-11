from typing import List, Optional
from sqlalchemy.orm import Session
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
