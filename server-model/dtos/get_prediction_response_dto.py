from typing import Optional
from pydantic import BaseModel


class PredictionDto(BaseModel):
    label: str
    probability: float


class GetPredictionResponseDto(BaseModel):
    prediction: PredictionDto
