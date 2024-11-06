import http
import json

from flask import Blueprint
from flask_injector import inject
from flask_cognito import cognito_auth_required
from pydantic import ValidationError

from services.interfaces.available_models_service import IAvailableModelsService
from utils.responses_helper import ok, bad_request, internal_server_error

bp = Blueprint("available_models", __name__, url_prefix="/available-models")


@bp.route(None, methods=[http.HTTPMethod.GET])
@cognito_auth_required
@inject
def get_available_models(available_models_service: IAvailableModelsService):
    try:
        return available_models_service.get_available_models()
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        print("Error:", e)
        return internal_server_error({"message": str(e)})
