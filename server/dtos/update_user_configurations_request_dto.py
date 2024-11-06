from pydantic import BaseModel, Field
from typing import Literal


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
    use_mediapipe_locally: bool = False
    use_right_arm_landscape: bool = False
    log_info: bool = False
    selected_model: Literal[
        "CMODEL",
        "CMODEL_2509",
        "CMODEL_2110",
        "CMODEL_2110_V2",
        "CMODEL_2310",
        "CMODEL_2510",
        "CMODEL_2810",
        "CMODEL_2910",
    ] = "CMODEL"
