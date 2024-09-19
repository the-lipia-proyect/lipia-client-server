from typing import Optional
from pydantic import BaseModel


class UpdateUserProfileRequestDto(BaseModel):
    name: str
    surname: str
    phone_number: Optional[str] = None
    phone_number_emergency: Optional[str] = ""
    phone_number_doctor: Optional[str] = ""
    phone_number_doctor_emergency: Optional[str] = ""
    blood_type: Optional[str] = ""
