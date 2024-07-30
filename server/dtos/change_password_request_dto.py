from pydantic import BaseModel


class ChangePasswordRequestDto(BaseModel):
    new_password: str
    actual_password: str
