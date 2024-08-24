from pydantic import BaseModel


class GenerateShortcutResponseDto(BaseModel):
    id: str
