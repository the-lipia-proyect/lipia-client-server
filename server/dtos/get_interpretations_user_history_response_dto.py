from pydantic import BaseModel
from typing import Optional


class WordDto(BaseModel):
    prediction: str
    order: int


class InterpretationDto(BaseModel):
    id: str
    word: WordDto
    note: Optional[str]
    created_at: float
    updated_at: float


class GetInterpretationsUserHistoryResponseDto(BaseModel):
    interpretations: list[InterpretationDto]
