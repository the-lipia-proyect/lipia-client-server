from typing import Optional
from pydantic import BaseModel


class UpdateUserProfileRequestDto(BaseModel):
    name: str
    surname: str
    phone_number: Optional[str] = None
