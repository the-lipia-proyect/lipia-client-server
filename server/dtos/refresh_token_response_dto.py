from pydantic import BaseModel


class RefreshTokenAuthResponseDto(BaseModel):
    access_token: str
    expiration_date: int
    id_token: str
    token_type: str


class RefreshTokenResponseDto(BaseModel):
    auth: RefreshTokenAuthResponseDto
