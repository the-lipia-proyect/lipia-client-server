from typing import Optional
from pydantic import BaseModel


class UpdateShortcutRequestDto(BaseModel):
    image: Optional[str] = None
    text: str
    order: Optional[int] = None
