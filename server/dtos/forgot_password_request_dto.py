from pydantic import BaseModel


class ForgotPasswordRequestDto(BaseModel):
    username: str
