import http
import os

from flask import jsonify, Blueprint, request

from utils.cognito_connector import CognitoUtils

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
        return (
            jsonify({"message": "Invalid body: missing 'username' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not password:
        return (
            jsonify({"message": "Invalid body: missing 'password' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
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
        return jsonify(response), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR


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
        return (
            jsonify({"message": "Invalid body: missing 'name' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not surname:
        return (
            jsonify({"message": "Invalid body: missing 'surname' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not phone_number:
        return (
            jsonify({"message": "Invalid body: missing 'phone_number' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not email:
        return (
            jsonify({"message": "Invalid body: missing 'email' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )

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
        response = {"id": user_id}
        return jsonify(response), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route(
    "/users/email-verification/verification-code-resend", methods=[http.HTTPMethod.POST]
)
def resend_email_confirmation_code():
    body = request.get_json()
    email = body.get(
        "email",
    )
    if not email:
        return (
            jsonify({"message": "Invalid body: missing 'email' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )

    try:
        cognito_utils.resend_confirmation_code(email)
        return jsonify({}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/users/email-verification", methods=[http.HTTPMethod.POST])
def verify_email():
    body = request.get_json()
    email = body.get(
        "email",
    )
    code = body.get("code")
    if not email:
        return (
            jsonify({"message": "Invalid body: missing 'email' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not code:
        return (
            jsonify({"message": "Invalid body: missing 'code' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )

    try:
        cognito_utils.verify_user(email, code)
        return jsonify({}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/users/refresh-token", methods=[http.HTTPMethod.POST])
def refresh_token():
    body = request.get_json()
    refresh_token = body.get(
        "refresh_token",
    )
    if not refresh_token:
        return (
            jsonify({"message": "Invalid body: missing 'refresh_token' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )

    try:
        refresh_token_response = cognito_utils.refresh_token(refresh_token)
        print("REFRESH_TOKEN_RESPONSE", refresh_token_response)
        return jsonify({}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/users/forgot-password", methods=[http.HTTPMethod.POST])
def forgot_password():
    body = request.get_json()
    username = body.get(
        "username",
    )
    if not username:
        return (
            jsonify({"message": "Invalid body: missing 'username' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )

    try:
        cognito_utils.forgot_password(username)
        return jsonify({}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route("/users/forgot-password/confirmation", methods=[http.HTTPMethod.POST])
def forgot_password_confirmation():
    body = request.get_json()
    username = body.get(
        "username",
    )
    password = body.get("password")
    code = body.get("code")
    if not username:
        return (
            jsonify({"message": "Invalid body: missing 'username' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not password:
        return (
            jsonify({"message": "Invalid body: missing 'password' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    if not code:
        return (
            jsonify({"message": "Invalid body: missing 'code' key"}),
            http.HTTPStatus.BAD_REQUEST,
        )
    try:
        cognito_utils.confirm_forgot_password(username, password, code)
        return jsonify({}), http.HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": e.__str__()}), http.HTTPStatus.INTERNAL_SERVER_ERROR
