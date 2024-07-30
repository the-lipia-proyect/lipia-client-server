from pydantic import BaseModel, Field, EmailStr, validator, ValidationError


class SignUpRequestDto(BaseModel):
    name: str
    surname: str
    phone_number: str
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8, max_length=20)

    @validator("password")
    def password_must_contain_uppercase_number_and_special_char(cls, v):
        print("V value:", v, cls)
        if (
            not any(c.isupper() for c in v)
            or not any(c.isdigit() for c in v)
            or not any(not c.isalnum() for c in v)
        ):
            raise ValueError(
                "The password should have at least one uppercase letter, one number and one special character"
            )
        return v
