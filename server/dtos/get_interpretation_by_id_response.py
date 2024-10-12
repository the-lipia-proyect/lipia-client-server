from .base_response_dto import BaseResponseDto
from typing import Optional, Any


class GetInterpretationByIdResponseDto(BaseResponseDto):
    note: Optional[str] = ""
    updated_at: int
    created_at: int
    frames: Any
