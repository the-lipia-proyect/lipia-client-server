from pydantic import BaseModel, Field


class SignUpRequestDto(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: str
    username: str
    password: str
