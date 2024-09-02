from typing import Optional, Any, Dict
from pydantic import BaseModel


class WordDto(BaseModel):
    prediction: str
    data: str


class Interpretation(BaseModel):
    words: list[WordDto]
    user_id: str
    updated_at: Optional[str] = None
    note: Optional[str] = None
