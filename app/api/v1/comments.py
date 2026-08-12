from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.comment_service import CommentService
from app.services.post_service import PostService

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crear un comentario en un post específico.
    Requiere autenticación.
    """
    # Verificar que el post existe
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    service = CommentService(db)
    return service.create_comment(
        comment_in, post_id=post_id, author_id=current_user.id
    )


@router.get("/", response_model=List[CommentResponse])
def list_comments(
    post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Listar comentarios de un post. Público.
    """
    # Verificar que el post existe
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    service = CommentService(db)
    return service.get_comments_by_post(post_id, skip=skip, limit=limit)


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    post_id: int,
    comment_id: int,
    comment_in: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Editar un comentario. Solo el autor puede editarlo.
    """
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    service = CommentService(db)
    comment = service.get_comment(comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return service.update_comment(comment, comment_in)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Eliminar un comentario. Solo el autor puede eliminarlo.
    """
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    service = CommentService(db)
    comment = service.get_comment(comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    service.delete_comment(comment)
    return None
