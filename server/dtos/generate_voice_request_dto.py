from pydantic import BaseModel, Field, validator, ValidationError
from typing import List


class GenerateVoiceRequestDto(BaseModel):
    name: str
    audios: List[str]  # Lista de cadenas sin restricción mínima

    @validator("audios")
    def check_audios_length(cls, value):
        if not value or len(value) < 1:
            raise ValueError("The list of audios must contain at least one element.")
        return value
