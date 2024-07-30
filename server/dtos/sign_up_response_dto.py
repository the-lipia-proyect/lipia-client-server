from pydantic import BaseModel


class SignUpResponseDto(BaseModel):
    id: str
