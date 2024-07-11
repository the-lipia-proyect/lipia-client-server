from flask import jsonify, Blueprint
import http
import os

from utils.api_caller import api_caller

bp = Blueprint("voices", __name__, url_prefix="/voices")

ELEVEN_LABS_URL = os.getenv("ELEVEN_LABS_API_URL")


@bp.route("/", methods=[http.HTTPMethod.GET])
def get():
    headers = {
        "Accept": "application/json",
        "xi-api-key": os.getenv("ELEVEN_LABS_API_KEY"),
        "Content-Type": "application/json",
    }
    response = api_caller(
        method=http.HTTPMethod.GET,
        url=f"{ELEVEN_LABS_URL}/voices",
        headers=headers,
    )

    voices = {
        "voices": [
            {"voice_id": item["voice_id"], "name": item["name"]}
            for item in response["voices"]
        ]
    }
    return jsonify(voices), http.HTTPStatus.OK


@bp.route("/", methods=[http.HTTPMethod.POST])
def post():
    response = {"message": "POST"}
    return jsonify(response), http.HTTPStatus.OK
