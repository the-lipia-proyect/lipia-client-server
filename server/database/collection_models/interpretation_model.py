from typing import Optional, Any, Dict
from pydantic import BaseModel


class WordDto(BaseModel):
    prediction: str
    order: int
    frames: Any


class Interpretation(BaseModel):
    word: Optional[WordDto] = None
    phrase_group: str
    user_id: str
    updated_at: Optional[str] = None
    note: Optional[str] = None
