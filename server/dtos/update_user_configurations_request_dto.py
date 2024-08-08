from pydantic import BaseModel, Field


class UpdateUserConfigurationsRequestDto(BaseModel):
    frame_delay: int = Field(..., ge=1, le=100)
    selected_voice: str
    selected_camera: str
    stability: float = 0.5
    similarity_boost: float = 0.95
    style: float = 0
