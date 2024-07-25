from flask import jsonify, Blueprint
import http

from utils.responses_helper import ok

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.route(None, methods=[http.HTTPMethod.GET])
def health():
    return ok({"message": "Healthy"})
