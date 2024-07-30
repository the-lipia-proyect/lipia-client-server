from pydantic import BaseModel


class ForgotPasswordConfirmationRequestDto(BaseModel):
    username: str
    password: str
    code: str
