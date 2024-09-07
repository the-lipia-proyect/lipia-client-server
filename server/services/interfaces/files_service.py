from abc import ABC, abstractmethod

from dtos.get_upload_presigned_url_response_dto import GetUploadPresignedUrlResponseDto
from dtos.get_upload_presigned_url_request_dto import GetUploadPresignedUrlRequestDto


class IFilesService(ABC):
    @abstractmethod
    def get_upload_presigned_url(
        self, req: GetUploadPresignedUrlRequestDto
    ) -> GetUploadPresignedUrlRequestDto:
        pass
