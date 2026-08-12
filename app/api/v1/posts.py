from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
import math
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostPagedResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crear un nuevo post. Requiere autenticación.
    El autor se asigna automáticamente al usuario logueado.
    """
    service = PostService(db)
    post = service.create_post(post_in, author_id=current_user.id)
    return post


@router.get("/", response_model=PostPagedResponse)
def list_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    author_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Listar posts con paginación, búsqueda y filtros.
    
    - page: número de página (empieza en 1)
    - size: cantidad por página
    - search: busca en título y contenido
    - status: draft | published | archived
    - category_id: filtrar por categoría
    - author_id: filtrar por autor
    """
    service = PostService(db)
    skip = (page - 1) * size
    
    items, total = service.search_posts(
        skip=skip,
        limit=size,
        search=search,
        status=status,
        category_id=category_id,
        author_id=author_id,
    )
    
    pages = math.ceil(total / size) if total > 0 else 0
    
    return PostPagedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Obtener un post por su ID.
    """
    service = PostService(db)
    post = service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/slug/{slug}", response_model=PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Obtener un post por su slug (URL amigable).
    """
    service = PostService(db)
    post = service.get_post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Editar un post. Requiere autenticación.
    """
    service = PostService(db)
    post = service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Por ahora cualquier usuario autenticado puede editar cualquier post.
    # En la semana 4 agregaremos: solo el autor o admin pueden editar.

    updated_post = service.update_post(post, post_in)
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Eliminar un post. Requiere autenticación.
    """
    service = PostService(db)
    post = service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    service.delete_post(post)
    return None
