from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.media import MediaResponse
from app.services.media_service import MediaService

router = APIRouter(prefix="/media", tags=["Media"])


@router.post(
    "/upload", response_model=MediaResponse, status_code=status.HTTP_201_CREATED
)
def upload_image(
    file: UploadFile = File(..., description="Image file to upload"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Subir una imagen al servidor.
    - Tipos permitidos: jpeg, png, gif, webp
    - Tamaño máximo: 5 MB
    - Requiere autenticación
    """
    service = MediaService(db)
    media = service.save_upload(file, uploader_id=current_user.id)
    return media


@router.get("/{media_id}", response_model=MediaResponse)
def get_media_info(media_id: int, db: Session = Depends(get_db)):
    """
    Obtener información de un archivo subido.
    """
    service = MediaService(db)
    media = service.get_media(media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media
