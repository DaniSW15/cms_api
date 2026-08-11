from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.tag import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.id == tag_id).first()

    def get_by_slug(self, slug: str) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.slug == slug).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        return self.db.query(Tag).offset(skip).limit(limit).all()

    def get_by_ids(self, ids: List[int]) -> List[Tag]:
        return self.db.query(Tag).filter(Tag.id.in_(ids)).all()

    def create(self, obj_in: dict) -> Tag:
        db_obj = Tag(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: Tag, obj_in: dict) -> Tag:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: Tag) -> None:
        self.db.delete(db_obj)
        self.db.commit()
