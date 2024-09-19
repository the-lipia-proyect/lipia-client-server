from pydantic import BaseModel


class GetUserProfileResponseDto(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: str
    is_premium: bool = True
    blood_type: str = ""
    phone_number_emergency: str = ""
    phone_number_doctor: str = ""
    phone_number_doctor_emergency: str = ""
