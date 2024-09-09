from typing import List

from pydantic import BaseModel


class VoiceDto(BaseModel):
    voice_id: str
    name: str
    category: str


class GetVoicesResponseDto(BaseModel):
    voices: List[VoiceDto]
