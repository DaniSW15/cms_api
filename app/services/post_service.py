from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.post_repo import PostRepository
from app.schemas.post import PostCreate, PostUpdate
from app.models.post import Post
from app.utils.slugify import slugify


class PostService:
    def __init__(self, db: Session):
        self.repo = PostRepository(db)

    def _generate_unique_slug(
        self, title: str, exclude_id: Optional[int] = None
    ) -> str:
        """Genera un slug único. Si ya existe, le agrega un número."""
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while True:
            existing = self.repo.get_by_slug(slug)
            if existing is None:
                return slug
            # Si estamos actualizando el mismo post, no cuenta como duplicado
            if exclude_id and existing.id == exclude_id:
                return slug
            slug = f"{base_slug}-{counter}"
            counter += 1

    def create_post(self, post_in: PostCreate, author_id: int) -> Post:
        post_data = post_in.model_dump(exclude={"tag_ids"})
        post_data["slug"] = self._generate_unique_slug(post_in.title)
        post_data["author_id"] = author_id

        post = self.repo.create(post_data)

        # Asignar tags si se enviaron
        if post_in.tag_ids:
            tags = self.tag_repo.get_by_ids(post_in.tag_ids)
            post.tags = tags
            self.repo.db.commit()
            self.repo.db.refresh(post)

        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.repo.get_by_id(post_id)

    def get_post_by_slug(self, slug: str) -> Optional[Post]:
        return self.repo.get_by_slug(slug)

    def get_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        return self.repo.get_multi(skip=skip, limit=limit)

    def update_post(self, post: Post, post_in: PostUpdate) -> Post:
        update_data = post_in.model_dump(exclude_unset=True, exclude={"tag_ids"})

        if "title" in update_data:
            update_data["slug"] = self._generate_unique_slug(
                update_data["title"], exclude_id=post.id
            )

        # Actualizar tags si se enviaron
        if post_in.tag_ids is not None:
            tags = self.tag_repo.get_by_ids(post_in.tag_ids)
            post.tags = tags

        return self.repo.update(post, update_data)

    def delete_post(self, post: Post) -> None:
        self.repo.delete(post)
