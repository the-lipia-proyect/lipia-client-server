from pydantic import BaseModel, Field


class VoiceSettingsDto(BaseModel):
    stability: float = 0.5
    similarity_boost: float = 0.95
    style: float = 0


class GenerateAudioFileRequestDto(BaseModel):
    text: str
    voice_id: str
    voice_settings: VoiceSettingsDto = Field(default_factory=VoiceSettingsDto)
