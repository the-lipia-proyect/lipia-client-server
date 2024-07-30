from pydantic import BaseModel


class LoginAuthResponseDto(BaseModel):
    access_token: str
    expiration_date: int
    id_token: str
    refresh_token: str
    token_type: str


class LoginResponseDto(BaseModel):
    auth: LoginAuthResponseDto
