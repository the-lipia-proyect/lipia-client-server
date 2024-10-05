from typing import Any
from pydantic import BaseModel


class GetLipnetPredictionRequestDto(BaseModel):
    frames: Any = None
