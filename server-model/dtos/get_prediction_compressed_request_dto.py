from pydantic import BaseModel


class GetPredictionCompressedRequestDto(BaseModel):
    data: str
