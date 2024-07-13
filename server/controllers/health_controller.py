from flask import jsonify, Blueprint
import http

bp = Blueprint("health", __name__, url_prefix="/health")


@bp.route(None, methods=[http.HTTPMethod.GET])
def health():
    response = {"message": "Healthy"}
    return jsonify(response), http.HTTPStatus.OK
