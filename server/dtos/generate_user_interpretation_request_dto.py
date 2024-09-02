from pydantic import BaseModel
from typing import Any


class WordDto(BaseModel):
    prediction: str
    data: str


class GenerateUserInterpretationRequestDto(BaseModel):
    words: list[WordDto]
