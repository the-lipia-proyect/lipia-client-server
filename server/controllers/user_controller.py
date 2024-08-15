import http

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from pydantic import ValidationError
from flask_injector import inject

from utils.responses_helper import bad_request, internal_server_error
from utils.auth_helper import get_authenticated_username
from services.interfaces.user_service import IUserService
from dtos.update_user_profile_request_dto import UpdateUserProfileRequestDto


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/profile", methods=[http.HTTPMethod.GET])
@cognito_auth_required
@inject
def get_user_profile(user_service: IUserService):
    try:
        return user_service.get_profile(get_authenticated_username())
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/profile", methods=[http.HTTPMethod.PUT])
@cognito_auth_required
@inject
def update_profile(user_service: IUserService):
    try:
        req = UpdateUserProfileRequestDto(**request.get_json())
        return user_service.update_profile(get_authenticated_username(), req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
