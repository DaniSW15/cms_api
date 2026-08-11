from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.models.category import Category
from app.utils.slugify import slugify


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

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

    def create_category(self, category_in: CategoryCreate) -> Category:
        data = category_in.model_dump()
        data["slug"] = self._generate_unique_slug(category_in.name)
        return self.repo.create(data)

    def get_category(self, category_id: int) -> Optional[Category]:
        return self.repo.get_by_id(category_id)

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.repo.get_multi(skip=skip, limit=limit)

    def update_category(
        self, category: Category, category_in: CategoryUpdate
    ) -> Category:
        update_data = category_in.model_dump(exclude_unset=True)
        if "name" in update_data:
            update_data["slug"] = self._generate_unique_slug(
                update_data["name"], exclude_id=category.id
            )
        return self.repo.update(category, update_data)

    def delete_category(self, category: Category) -> None:
        self.repo.delete(category)
