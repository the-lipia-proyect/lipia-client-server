import http
import os

from flask import Blueprint, request
from flask_cognito import cognito_auth_required
from pydantic import ValidationError

from utils.cognito_connector import CognitoUtils
from utils.responses_helper import ok, bad_request, internal_server_error
from utils.auth_helper import get_authenticated_username, get_access_token
from dtos.login_request_dto import LoginRequestDto
from dtos.login_response_dto import LoginResponseDto, LoginAuthResponseDto
from dtos.sign_up_request_dto import SignUpRequestDto
from dtos.sign_up_response_dto import SignUpResponseDto
from dtos.verification_code_resend_request_dto import VerificationCodeResendRequestDto
from dtos.email_verification_request_dto import EmailVerificationRequestDto
from dtos.refresh_token_dto import RefreshTokenRequestDto
from dtos.refresh_token_response_dto import (
    RefreshTokenResponseDto,
    RefreshTokenAuthResponseDto,
)
from dtos.forgot_password_request_dto import ForgotPasswordRequestDto
from dtos.forgot_password_confirmation_request_dto import (
    ForgotPasswordConfirmationRequestDto,
)
from dtos.change_password_request_dto import ChangePasswordRequestDto

cognito_utils = CognitoUtils(
    os.getenv("AWS_COGNITO_USERS_POOL_ID"), os.getenv("AWS_COGNITO_USERS_CLIENT_ID")
)

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/users/login", methods=[http.HTTPMethod.POST])
def login():

    try:
        req = LoginRequestDto(**request.get_json())
        authenticate_user_response = cognito_utils.authenticate_user(
            req.username, req.password
        )
        response = LoginResponseDto(
            auth=LoginAuthResponseDto(
                access_token=authenticate_user_response.get("AccessToken"),
                expiration_date=authenticate_user_response.get("ExpiresIn"),
                id_token=authenticate_user_response.get("IdToken"),
                refresh_token=authenticate_user_response.get("RefreshToken"),
                token_type=authenticate_user_response.get("TokenType"),
            )
        ).model_dump()
        return ok(response)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/sign-up", methods=[http.HTTPMethod.POST])
def sign_up():

    try:
        req = SignUpRequestDto(**request.get_json())
        register_user_dto = {
            "name": req.name,
            "surname": req.surname,
            "email": req.email,
            "phone_number": req.phone_number,
            "username": req.username,
            "password": req.password,
        }
        user_id = cognito_utils.register_user(register_user_dto)
        return ok(SignUpResponseDto(id=user_id).model_dump())
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route(
    "/users/email-verification/verification-code-resend", methods=[http.HTTPMethod.POST]
)
def resend_email_confirmation_code():
    try:
        req = VerificationCodeResendRequestDto(**request.get_json())
        cognito_utils.resend_confirmation_code(req.email)
        return ok({})
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/email-verification", methods=[http.HTTPMethod.POST])
def verify_email():
    try:
        req = EmailVerificationRequestDto(**request.get_json())
        cognito_utils.verify_user(req.email, req.code)
        return ok({})
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/refresh-token", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def refresh_token():
    username = get_authenticated_username()

    try:
        req = RefreshTokenRequestDto(**request.get_json())
        refresh_token_response = cognito_utils.refresh_token(
            username, req.refresh_token
        )
        response = RefreshTokenResponseDto(
            auth=RefreshTokenAuthResponseDto(
                access_token=refresh_token_response.get("AccessToken"),
                expiration_date=refresh_token_response.get("ExpiresIn"),
                id_token=refresh_token_response.get("IdToken"),
                token_type=refresh_token_response.get("TokenType"),
            )
        ).model_dump()
        return ok(response)
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/forgot-password", methods=[http.HTTPMethod.POST])
def forgot_password():
    try:
        req = ForgotPasswordRequestDto(**request.get_json())
        cognito_utils.forgot_password(req.username)
        return ok({})
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/forgot-password/confirmation", methods=[http.HTTPMethod.POST])
def forgot_password_confirmation():
    try:
        req = ForgotPasswordConfirmationRequestDto(**request.get_json())
        cognito_utils.confirm_forgot_password(req.username, req.password, req.code)
        return ok({})
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/change-password", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def change_password():
    try:
        req = ChangePasswordRequestDto(**request.get_json())
        access_token = get_access_token()
        # TODO: Add auth token as the first parameter
        cognito_utils.change_password(
            access_token,
            req.new_password,
            req.actual_password,
        )
        return ok({})
    except ValidationError as e:
        return bad_request({"message": e.errors()})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
