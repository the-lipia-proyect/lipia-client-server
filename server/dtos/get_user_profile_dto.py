from pydantic import BaseModel


class GetUserProfileResponseDto(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: str
    is_premium: bool = True
