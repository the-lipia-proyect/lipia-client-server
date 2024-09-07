from pydantic import BaseModel
from typing import Optional


class GetUploadPresignedUrlRequestDto(BaseModel):
    content_type: Optional[str] = None
    extension: Optional[str] = None
