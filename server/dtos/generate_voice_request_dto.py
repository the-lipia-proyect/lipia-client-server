from pydantic import BaseModel, Field


class GenerateVoiceRequestDto(BaseModel):
    name: str
