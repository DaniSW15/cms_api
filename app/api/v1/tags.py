from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(tag_in: TagCreate, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.create_tag(tag_in)


@router.get("/", response_model=List[TagResponse])
def list_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.get_tags(skip=skip, limit=limit)


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    service = TagService(db)
    tag = service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag_in: TagUpdate, db: Session = Depends(get_db)):
    service = TagService(db)
    tag = service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return service.update_tag(tag, tag_in)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    service = TagService(db)
    tag = service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    service.delete_tag(tag)
    return None
