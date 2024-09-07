import http

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from flask_injector import inject
from pydantic import ValidationError

from utils.auth_helper import get_user_id
from utils.responses_helper import bad_request, internal_server_error
from dtos.get_upload_presigned_url_request_dto import GetUploadPresignedUrlRequestDto
from services.interfaces.files_service import IFilesService


bp = Blueprint("files", __name__, url_prefix="/files")


@bp.route("/presigned-url", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def get_upload_presigned_url(utils_service: IFilesService):
    try:
        req = GetUploadPresignedUrlRequestDto(**request.get_json())
        return utils_service.get_upload_presigned_url(req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
