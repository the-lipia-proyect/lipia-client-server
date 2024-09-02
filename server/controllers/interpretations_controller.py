import http

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from pydantic import ValidationError
from flask_injector import inject

from utils.responses_helper import bad_request, internal_server_error, ok
from utils.auth_helper import get_user_id
from services.interfaces.interpretation_service import IInterpretationService
from dtos.generate_user_interpretation_request_dto import (
    GenerateUserInterpretationRequestDto,
)
from dtos.update_interpretation_note_request_dto import (
    UpdateInterpretationNoteRequestDto,
)


bp = Blueprint("interpretations", __name__, url_prefix="/interpretations")


@bp.route("/user_history", methods=[http.HTTPMethod.GET])
@cognito_auth_required
@inject
def get_interpretations_user_history(interpretation_service: IInterpretationService):
    try:
        order_by = request.args.get("order_by", default="order")
        descending_order = (
            request.args.get("descending_order", default="false").lower() == "true"
        )
        page = request.args.get("page", default="1")
        page_size = request.args.get("page_size", default=None)
        try:
            page = int(page)
        except ValueError:
            page = 1

        try:
            page_size = int(page_size) if page_size is not None else None
        except ValueError:
            page_size = None
        return interpretation_service.get_user_history(
            get_user_id(), order_by, descending_order, page, page_size
        )
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route(None, methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_create_interpretation(interpretation_service: IInterpretationService):
    try:
        req = GenerateUserInterpretationRequestDto(**request.get_json())
        return interpretation_service.insert_user_interpretation(get_user_id(), req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("<string:id>/notes", methods=[http.HTTPMethod.PUT])
@cognito_auth_required
@inject
def put_update_interpretation_note(
    id: str, interpretation_service: IInterpretationService
):
    try:
        req = UpdateInterpretationNoteRequestDto(**request.get_json())
        return interpretation_service.update_interpretation_note(id, req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
