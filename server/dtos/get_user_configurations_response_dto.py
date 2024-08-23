from pydantic import BaseModel


class GetUserConfigurationsResponseDto(BaseModel):
    frame_delay: int = 1
    selected_camera: str
    selected_voice: str
    stability: float = 0.5
    similarity_boost: float = 0.95
    style: float = 0
    words_timeout: int = 5
    use_custom_voice: bool = False
    facing_mode: str = "user"
