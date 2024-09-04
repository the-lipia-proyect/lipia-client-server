from pydantic import BaseModel


class BaseResponseDto(BaseModel):
    id: str
