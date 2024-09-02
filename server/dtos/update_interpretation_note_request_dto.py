from pydantic import BaseModel, Field


class UpdateInterpretationNoteRequestDto(BaseModel):
    note: str = Field(..., min_length=1)
