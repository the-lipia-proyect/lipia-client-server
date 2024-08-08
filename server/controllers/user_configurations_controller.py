import http

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from pydantic import ValidationError
from flask_injector import inject

from utils.responses_helper import bad_request, internal_server_error
from utils.auth_helper import get_authenticated_username
from services.interfaces.user_configurations_service import IUserConfigurationService
from dtos.update_user_configurations_request_dto import (
    UpdateUserConfigurationsRequestDto,
)


bp = Blueprint("user_configurations", __name__, url_prefix="/user_configurations")


@bp.route(None, methods=[http.HTTPMethod.GET])
@cognito_auth_required
@inject
def get_user_configurations(user_configuration_service: IUserConfigurationService):
    try:
        return user_configuration_service.get_user_configurations_by_user_id(
            get_authenticated_username()
        )
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route(None, methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_user_configurations(user_configuration_service: IUserConfigurationService):
    try:
        req = UpdateUserConfigurationsRequestDto(**request.get_json())
        return user_configuration_service.update_user_configuration(
            get_authenticated_username(), req
        )
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
