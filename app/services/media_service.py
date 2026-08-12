import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.media import Media


class MediaService:
    def __init__(self, db: Session):
        self.db = db

    def _validate_file(self, file: UploadFile) -> None:
        """
        Valida tipo y tamaño del archivo antes de guardarlo.
        """
        # Validar tipo de contenido
        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_IMAGE_TYPES)}",
            )

        # Validar tamaño (lee los primeros bytes para estimar)
        file.file.seek(0, 2)  # Mover al final
        file_size = file.file.tell()
        file.file.seek(0)  # Volver al inicio

        if file_size > settings.MAX_UPLOAD_SIZE:
            max_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {max_mb} MB",
            )

    def save_upload(self, file: UploadFile, uploader_id: int) -> Media:
        """
        Guarda el archivo en disco y registra en la base de datos.
        """
        self._validate_file(file)

        # Crear nombre único para evitar colisiones
        extension = Path(file.filename).suffix
        unique_name = f"{uuid.uuid4().hex}{extension}"

        # Asegurar que la carpeta uploads existe
        upload_dir = settings.upload_path
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / unique_name

        # Guardar archivo en disco
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Construir URL pública
        file_url = f"/uploads/{unique_name}"

        # Guardar en base de datos
        db_media = Media(
            original_filename=file.filename,
            stored_filename=unique_name,
            file_path=str(file_path),
            content_type=file.content_type,
            size=file_path.stat().st_size,
            url=file_url,
        )
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    def get_media(self, media_id: int) -> Media | None:
        return self.db.query(Media).filter(Media.id == media_id).first()
