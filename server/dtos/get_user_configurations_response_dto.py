from pydantic import BaseModel


class GetUserConfigurationsResponseDto(BaseModel):
    frame_delay: int = 0
    selected_camera: str
    selected_voice: str
    stability: float = 0.5
    similarity_boost: float = 0.95
    playback_rate: float = 0.5
    style: float = 0
    words_timeout: int = 3
    use_custom_voice: bool = False
    facing_mode: str = "user"
    enable_emergency_phones: bool = False
    mouth_open_threshold: int = 20
    interpreter_always_active: bool = False
    interpreter_compress_frames: bool = False
    use_lipnet_model: bool = False
    use_mediapipe_locally: bool = False
    use_right_arm_landscape: bool = False
    log_info: bool = False
    selected_model: str = "CMODEL"
