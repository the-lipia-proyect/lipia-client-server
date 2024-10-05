from typing import Optional
from pydantic import BaseModel


class UpdateUserProfileRequestDto(BaseModel):
    name: str
    surname: str
    phone_number: str = ""
    phone_number_emergency: str = ""
    phone_number_doctor: Optional[str] = ""
    phone_number_doctor_emergency: Optional[str] = ""
    blood_type: str = ""
