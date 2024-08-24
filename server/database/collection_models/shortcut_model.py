from typing import Optional
from pydantic import BaseModel


class Shortcut(BaseModel):
    image: Optional[str] = None
    text: str
    order: int
    audio_file_url: Optional[str] = None
    voice_description: Optional[str] = None
    user_id: str
    updated_at: Optional[str] = None
