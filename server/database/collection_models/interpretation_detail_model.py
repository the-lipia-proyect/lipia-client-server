from typing import Any
from pydantic import BaseModel


class InterpretationDetail(BaseModel):
    id: str
    frames: Any
