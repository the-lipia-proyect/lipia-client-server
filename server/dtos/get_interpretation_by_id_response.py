from .base_response_dto import BaseResponseDto


class GetInterpretationByIdResponseDto(BaseResponseDto):
    note: str
    updated_at: int
    created_at: int
