from typing import Optional
from pydantic import BaseModel


class ShortcutDto(BaseModel):
    id: str
    text: str
    image_url: Optional[str] = None
    order: int
    audio_file_url: Optional[str] = None
    voice_description: Optional[str] = None


class GetUserShortcutsResponseDto(BaseModel):
    shortcuts: list[ShortcutDto]
