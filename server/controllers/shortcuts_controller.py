import http

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from pydantic import ValidationError
from flask_injector import inject

from utils.responses_helper import bad_request, internal_server_error
from utils.auth_helper import get_user_id
from services.interfaces.shortcuts_service import IShortcutsService
from dtos.generate_shortcut_request_dto import GenerateShortcutRequestDto
from dtos.update_shortcut_request_dto import UpdateShortcutRequestDto


bp = Blueprint("shortcuts", __name__, url_prefix="/shortcuts")


@bp.route(None, methods=[http.HTTPMethod.GET])
@cognito_auth_required
@inject
def get_user_shortcurts(shortcuts_service: IShortcutsService):
    try:
        order_by = request.args.get("order_by", default="order")
        descending_order = (
            request.args.get("descending_order", default="false").lower() == "true"
        )
        return shortcuts_service.get_user_shortcuts(
            get_user_id(), order_by, descending_order
        )
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route(None, methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_user_configurations(shortcuts_service: IShortcutsService):
    try:
        req = GenerateShortcutRequestDto(**request.get_json())
        return shortcuts_service.insert_user_shortcut(get_user_id(), req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/<string:id>", methods=[http.HTTPMethod.PUT])
@cognito_auth_required
@inject
def put_user_configurations(id: str, shortcuts_service: IShortcutsService):
    try:
        req = UpdateShortcutRequestDto(**request.get_json())
        return shortcuts_service.update_user_shortcut(id, get_user_id(), req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/<string:id>", methods=[http.HTTPMethod.DELETE])
@cognito_auth_required
@inject
def delete_user_configurations(id: str, shortcuts_service: IShortcutsService):
    try:
        return shortcuts_service.delete_user_shortcut(id)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
