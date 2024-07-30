from pydantic import BaseModel


class GenerateAudioFileResponseDto(BaseModel):
    file_url: str
