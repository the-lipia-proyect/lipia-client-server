from typing import List
from pydantic import BaseModel


class GetAvailableModelsResponseDto(BaseModel):
    models: List[str]
