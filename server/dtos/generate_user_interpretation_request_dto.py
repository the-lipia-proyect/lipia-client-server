from pydantic import BaseModel
from typing import Any


class WordDto(BaseModel):
    prediction: str
    order: int


class GenerateUserInterpretationRequestDto(BaseModel):
    word: WordDto
    phrase_group: str
