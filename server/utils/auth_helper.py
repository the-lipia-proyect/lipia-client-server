from dotenv import load_dotenv
from flask import request
from flask_cognito import current_cognito_jwt

load_dotenv()


def get_authenticated_username():
    return current_cognito_jwt.get("username")


def get_access_token():
    if request.headers["Authorization"]:
        return request.headers.get("Authorization").split(" ")[1]
