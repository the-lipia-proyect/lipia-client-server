from pydantic import BaseModel, Field


class UpdateUserConfigurationsRequestDto(BaseModel):
    frame_delay: int = Field(..., ge=0, le=100)
    selected_voice: str
    selected_camera: str
    stability: float = 0.5
    similarity_boost: float = 0.95
    playback_rate: float = Field(0.5, ge=0, le=1)
    style: float = 0
    words_timeout: int = Field(..., ge=0, le=10)
    use_custom_voice: bool
    facing_mode: str = "user"
    enable_emergency_phones: bool = False
    interpreter_always_active: bool = False
    mouth_open_threshold: int = 20
    interpreter_compress_frames: bool = False
    use_lipnet_model: bool = False
