from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.comment_repo import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate
from app.models.comment import Comment


class CommentService:
    def __init__(self, db: Session):
        self.repo = CommentRepository(db)

    def create_comment(
        self, comment_in: CommentCreate, post_id: int, author_id: int
    ) -> Comment:
        data = comment_in.model_dump()
        data["post_id"] = post_id
        data["author_id"] = author_id
        return self.repo.create(data)

    def get_comments_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return self.repo.get_by_post(post_id, skip=skip, limit=limit)

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        return self.repo.get_by_id(comment_id)

    def update_comment(self, comment: Comment, comment_in: CommentUpdate) -> Comment:
        return self.repo.update(comment, comment_in.model_dump())

    def delete_comment(self, comment: Comment) -> None:
        self.repo.delete(comment)
