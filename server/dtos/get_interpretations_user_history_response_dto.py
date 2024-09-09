from pydantic import BaseModel


class WordDto(BaseModel):
    prediction: str
    order: int


class InterpretationDto(BaseModel):
    id: str
    word: WordDto
    created_at: float
    updated_at: float
    phrase_group: str


class GetInterpretationsUserHistoryResponseDto(BaseModel):
    interpretations: list[InterpretationDto]
