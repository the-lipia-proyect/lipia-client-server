from pydantic import BaseModel


class VerificationCodeResendRequestDto(BaseModel):
    email: str
