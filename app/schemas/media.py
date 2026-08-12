from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    stored_filename: str
    content_type: str
    size: int
    url: str
    created_at: datetime
