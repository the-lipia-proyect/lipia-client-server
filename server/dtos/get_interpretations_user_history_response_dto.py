from pydantic import BaseModel
from typing import Optional, Any


class WordDto(BaseModel):
    prediction: str
    data: Any


class InterpretationDto(BaseModel):
    id: str
    words: list[WordDto]
    note: Optional[str]
    created_at: float
    updated_at: float


class GetInterpretationsUserHistoryResponseDto(BaseModel):
    interpretations: list[InterpretationDto]
