from pydantic import BaseModel


class GetUploadPresignedUrlResponseDto(BaseModel):
    presigned_url: str
