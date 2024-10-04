from typing import Any
from pydantic import BaseModel


class GetPredictionRequestDto(BaseModel):
    model: str = "CMODEL"
    frames: Any = None
    with_rgb: bool = False
