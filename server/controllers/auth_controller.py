import http
import json

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from pydantic import ValidationError
from flask_injector import inject

from utils.responses_helper import ok, bad_request, internal_server_error
from utils.auth_helper import get_authenticated_username, get_access_token
from dtos.login_request_dto import LoginRequestDto
from dtos.sign_up_request_dto import SignUpRequestDto
from dtos.verification_code_resend_request_dto import VerificationCodeResendRequestDto
from dtos.email_verification_request_dto import EmailVerificationRequestDto
from dtos.refresh_token_dto import RefreshTokenRequestDto
from dtos.forgot_password_request_dto import ForgotPasswordRequestDto
from dtos.forgot_password_confirmation_request_dto import (
    ForgotPasswordConfirmationRequestDto,
)
from dtos.change_password_request_dto import ChangePasswordRequestDto
from services.interfaces.auth_service import IAuthService


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/users/login", methods=[http.HTTPMethod.POST])
@inject
def login(auth_service: IAuthService):
    try:
        req = LoginRequestDto(**request.get_json())
        return auth_service.login(req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/sign-up", methods=[http.HTTPMethod.POST])
@inject
def sign_up(auth_service: IAuthService):
    try:
        req = SignUpRequestDto(**request.get_json())
        return auth_service.sign_up(req)
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route(
    "/users/email-verification/verification-code-resend", methods=[http.HTTPMethod.POST]
)
@inject
def resend_email_confirmation_code(auth_service: IAuthService):
    try:
        req = VerificationCodeResendRequestDto(**request.get_json())
        return auth_service.resend_email_confirmation_code(req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/email-verification", methods=[http.HTTPMethod.POST])
@inject
def verify_email(auth_service: IAuthService):
    try:
        req = EmailVerificationRequestDto(**request.get_json())
        auth_service.verify_email(req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/refresh-token", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def refresh_token(auth_service: IAuthService):

    try:
        req = RefreshTokenRequestDto(**request.get_json())
        username = get_authenticated_username()
        return auth_service.refresh_token(username, req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/forgot-password", methods=[http.HTTPMethod.POST])
@inject
def forgot_password(auth_service: IAuthService):
    try:
        req = ForgotPasswordRequestDto(**request.get_json())
        return auth_service.forgot_password(req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/forgot-password/confirmation", methods=[http.HTTPMethod.POST])
@inject
def forgot_password_confirmation(auth_service: IAuthService):
    try:
        req = ForgotPasswordConfirmationRequestDto(**request.get_json())
        return auth_service.forgot_password_confirmation(req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/change-password", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def change_password(auth_service: IAuthService):
    try:
        access_token = get_access_token()
        req = ChangePasswordRequestDto(**request.get_json())
        return auth_service.change_password(access_token, req)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
