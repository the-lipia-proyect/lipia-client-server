from typing import Optional
from pydantic import BaseModel


class ShortcutDto(BaseModel):
    id: str
    text: str
    image_url: Optional[str] = None
    order: Optional[int] = None
    audio_file_url: Optional[str] = None
    voice_description: Optional[str] = None
    created_at: float
    updated_at: float


class GetUserShortcutsResponseDto(BaseModel):
    shortcuts: list[ShortcutDto]
