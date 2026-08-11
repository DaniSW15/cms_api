from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.tag_repo import TagRepository
from app.schemas.tag import TagCreate, TagUpdate
from app.models.tag import Tag
from app.utils.slugify import slugify


class TagService:
    def __init__(self, db: Session):
        self.repo = TagRepository(db)

    def _generate_unique_slug(self, name: str, exclude_id: Optional[int] = None) -> str:
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while True:
            existing = self.repo.get_by_slug(slug)
            if existing is None or (exclude_id and existing.id == exclude_id):
                return slug
            slug = f"{base_slug}-{counter}"
            counter += 1

    def create_tag(self, tag_in: TagCreate) -> Tag:
        data = tag_in.model_dump()
        data["slug"] = self._generate_unique_slug(tag_in.name)
        return self.repo.create(data)

    def get_tag(self, tag_id: int) -> Optional[Tag]:
        return self.repo.get_by_id(tag_id)

    def get_tags(self, skip: int = 0, limit: int = 100) -> List[Tag]:
        return self.repo.get_multi(skip=skip, limit=limit)

    def get_tags_by_ids(self, ids: List[int]) -> List[Tag]:
        return self.repo.get_by_ids(ids)

    def update_tag(self, tag: Tag, tag_in: TagUpdate) -> Tag:
        update_data = tag_in.model_dump(exclude_unset=True)
        if "name" in update_data:
            update_data["slug"] = self._generate_unique_slug(
                update_data["name"], exclude_id=tag.id
            )
        return self.repo.update(tag, update_data)

    def delete_tag(self, tag: Tag) -> None:
        self.repo.delete(tag)
