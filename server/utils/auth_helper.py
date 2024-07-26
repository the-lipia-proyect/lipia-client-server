import os
import requests
import jwt

from dotenv import load_dotenv
from flask import request

from utils.responses_helper import forbidden

load_dotenv()

keys = requests.get(os.getenv("AWS_COGNITO_KEYS_URL")).json()["keys"]


def get_public_key(kid):
    for key in keys:
        if key["kid"] == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key)
    return None


def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split()[1]

        if not token:
            return forbidden({"message": "Token is missing"})
        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_public_key = get_public_key(unverified_header["kid"])
            payload = jwt.decode(
                token,
                rsa_public_key,
                algorithms=["RS256"],
                # TODO: Analyze if this prop is necessary
                # audience=os.getenv("AWS_COGNITO_USERS_CLIENT_ID"),
            )
            request.user = payload
        except jwt.ExpiredSignatureError:
            return forbidden({"message": "Token has expired"})
        except jwt.InvalidTokenError as error:
            print("ERROR", error)
            return forbidden({"message": "Invalid token"})

        return f(*args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator


def verify_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_public_key = get_public_key(unverified_header["kid"])
        if rsa_public_key is None:
            raise ValueError("Public key not found.")

        payload = jwt.decode(token, rsa_public_key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def get_username_from_token(token: str):
    return verify_token(token)["username"]


def get_access_token():
    if request.headers["Authorization"]:
        return request.headers.get("Authorization").split(" ")[1]
