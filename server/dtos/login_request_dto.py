from pydantic import BaseModel, Field


class LoginRequestDto(BaseModel):
    username: str = Field(...)
    password: str
