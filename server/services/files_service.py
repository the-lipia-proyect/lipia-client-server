from flask_injector import inject
import uuid

from utils.responses_helper import ok, not_found
from .interfaces.s3_service import IS3Service
from .interfaces.files_service import IFilesService
from dtos.get_upload_presigned_url_response_dto import GetUploadPresignedUrlResponseDto
from dtos.get_upload_presigned_url_request_dto import GetUploadPresignedUrlRequestDto

S3_PUT_OBJECT_CLIENT_METHOD = "put_object"
TEMP_FOLDER_PATH = "temp"


class FilesService(IFilesService):
    @inject
    def __init__(self, s3_service: IS3Service):
        self._s3_service = s3_service

    def get_upload_presigned_url(
        self, req: GetUploadPresignedUrlRequestDto
    ) -> GetUploadPresignedUrlResponseDto:
        file_name = f"{TEMP_FOLDER_PATH}/{str(uuid.uuid4())}"
        if req.extension:
            file_name += f".{req.extension}"
        presigned_url = self._s3_service.generate_presigned_url(
            S3_PUT_OBJECT_CLIENT_METHOD,
            file_name=file_name,
            params={"ContentType": req.content_type} if req.content_type else None,
        )
        response = GetUploadPresignedUrlResponseDto(presigned_url=presigned_url)
        return ok(response)
