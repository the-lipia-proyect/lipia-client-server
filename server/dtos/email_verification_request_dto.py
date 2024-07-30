from pydantic import BaseModel


class EmailVerificationRequestDto(BaseModel):
    email: str
    code: str
