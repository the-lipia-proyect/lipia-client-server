import http
import os

from flask import Blueprint, request
from flask_cognito import cognito_auth_required

from utils.cognito_connector import CognitoUtils
from utils.responses_helper import ok, bad_request, internal_server_error
from utils.auth_helper import (
    get_access_token,
    get_authenticated_username,
)

cognito_utils = CognitoUtils(
    os.getenv("AWS_COGNITO_USERS_POOL_ID"), os.getenv("AWS_COGNITO_USERS_CLIENT_ID")
)

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/users/login", methods=[http.HTTPMethod.POST])
def login():
    body = request.get_json()
    username = body.get(
        "username",
    )
    password = body.get("password")
    if not username:
        return bad_request({"message": "Invalid body: missing 'username' key"})
    if not password:
        return bad_request({"message": "Invalid body: missing 'password' key"})
    try:
        authenticate_user_response = cognito_utils.authenticate_user(username, password)
        response = {
            "auth": {
                "access_token": authenticate_user_response.get("AccessToken"),
                "expiration_date": authenticate_user_response.get("ExpiresIn"),
                "id_token": authenticate_user_response.get("IdToken"),
                "refresh_token": authenticate_user_response.get("RefreshToken"),
                "token_type": authenticate_user_response.get("TokenType"),
            }
        }
        return ok(response)
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/sign-up", methods=[http.HTTPMethod.POST])
def sign_up():
    body = request.get_json()
    name = body.get(
        "name",
    )
    surname = body.get("surname")
    phone_number = body.get("phone_number")
    email = body.get("email")
    username = body.get("username")
    password = body.get("password")
    if not name:
        return bad_request({"message": "Invalid body: missing 'name' key"})
    if not surname:
        return bad_request({"message": "Invalid body: missing 'surname' key"})
    if not phone_number:
        return bad_request({"message": "Invalid body: missing 'phone_number' key"})
    if not email:
        return bad_request({"message": "Invalid body: missing 'email' key"})
    if not username:
        return bad_request({"message": "Invalid body: missing 'username' key"})
    if not password:
        return bad_request({"message": "Invalid body: missing 'password' key"})

    register_user_dto = {
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone_number,
        "username": username,
        "password": password,
    }
    try:
        user_id = cognito_utils.register_user(register_user_dto)
        return ok({"id": user_id})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route(
    "/users/email-verification/verification-code-resend", methods=[http.HTTPMethod.POST]
)
def resend_email_confirmation_code():
    body = request.get_json()
    email = body.get(
        "email",
    )
    if not email:
        return bad_request({"message": "Invalid body: missing 'email' key"})

    try:
        cognito_utils.resend_confirmation_code(email)
        return ok({})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/email-verification", methods=[http.HTTPMethod.POST])
def verify_email():
    body = request.get_json()
    email = body.get(
        "email",
    )
    code = body.get("code")
    if not email:
        return bad_request({"message": "Invalid body: missing 'email' key"})
    if not code:
        return bad_request({"message": "Invalid body: missing 'code' key"})

    try:
        cognito_utils.verify_user(email, code)
        return ok({})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/refresh-token", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def refresh_token():
    body = request.get_json()
    refresh_token = body.get(
        "refresh_token",
    )
    username = get_authenticated_username()
    if not refresh_token:
        return bad_request({"message": "Invalid body: missing 'refresh_token' key"})

    try:
        refresh_token_response = cognito_utils.refresh_token(username, refresh_token)
        response = {
            "auth": {
                "access_token": refresh_token_response.get("AccessToken"),
                "expiration_date": refresh_token_response.get("ExpiresIn"),
                "id_token": refresh_token_response.get("IdToken"),
                "token_type": refresh_token_response.get("TokenType"),
            }
        }
        return ok(response)
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/forgot-password", methods=[http.HTTPMethod.POST])
def forgot_password():
    body = request.get_json()
    username = body.get(
        "username",
    )
    if not username:
        return bad_request({"message": "Invalid body: missing 'username' key"})

    try:
        cognito_utils.forgot_password(username)
        return ok({})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/forgot-password/confirmation", methods=[http.HTTPMethod.POST])
def forgot_password_confirmation():
    body = request.get_json()
    username = body.get(
        "username",
    )
    password = body.get("password")
    code = body.get("code")
    if not username:
        return bad_request({"message": "Invalid body: missing 'username' key"})
    if not password:
        return bad_request({"message": "Invalid body: missing 'password' key"})
    if not code:
        return bad_request({"message": "Invalid body: missing 'code' key"})
    try:
        cognito_utils.confirm_forgot_password(username, password, code)
        return ok({})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})


@bp.route("/users/change-password", methods=[http.HTTPMethod.POST])
@cognito_auth_required
def change_password():
    body = request.get_json()
    new_password = body.get(
        "new_password",
    )
    actual_password = body.get(
        "actual_password",
    )
    access_token = get_access_token()
    if not new_password:
        return bad_request({"message": "Invalid body: missing 'new_password' key"})
    if not actual_password:
        return bad_request({"message": "Invalid body: missing 'actual_password' key"})
    try:
        # TODO: Add auth token as the first parameter
        cognito_utils.change_password(
            access_token,
            new_password,
            actual_password,
        )
        return ok({})
    except Exception as e:
        return internal_server_error({"message": e.__str__()})
