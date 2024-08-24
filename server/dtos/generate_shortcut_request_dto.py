from typing import Optional
from pydantic import BaseModel


class GenerateShortcutRequestDto(BaseModel):
    image: Optional[str] = None
    text: str
    order: int
