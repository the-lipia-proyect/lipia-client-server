import http

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from flask_injector import inject
from pydantic import ValidationError

from services.interfaces.voices_service import IVoicesService
from utils.auth_helper import get_user_id
from utils.responses_helper import bad_request, internal_server_error
from dtos.generate_audio_file_request_dto import GenerateAudioFileRequestDto
from dtos.generate_voice_request_dto import GenerateVoiceRequestDto


bp = Blueprint("voices", __name__, url_prefix="/voices")


@bp.route(None, methods=[http.HTTPMethod.GET])
@cognito_auth_required
@inject
def get_voices(voices_service: IVoicesService):
    try:
        return voices_service.get_voices(
            get_user_id(),
        )
    except Exception as e:
        print("Error:", e)
        return internal_server_error(str(e))


@bp.route(None, methods=[http.HTTPMethod.POST])
@cognito_auth_required
def generate_voice(voices_service: IVoicesService):
    try:
        req = GenerateVoiceRequestDto(**request.get_json())
        return voices_service.create_voice(get_user_id(), req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        print("Error:", e)
        return internal_server_error(str(e))


@bp.route("<string:id>", methods=[http.HTTPMethod.DELETE])
@cognito_auth_required
def delete_voice(id: str, voices_service: IVoicesService):
    try:
        return voices_service.delete_voice(get_user_id(), id)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        print("Error:", e)
        return internal_server_error(str(e))


@bp.route("/text-to-speech", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def generate_audio_file(voices_service: IVoicesService):
    try:
        req = GenerateAudioFileRequestDto(**request.get_json())
        return voices_service.generate_audio_file(get_user_id(), req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        print("Error:", e)
        return internal_server_error(str(e))
