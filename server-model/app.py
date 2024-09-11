import os
from flask import Flask, Blueprint

from flask_cors import CORS
import awsgi
from controllers import health_controller, predictions_controller


API_VERSION = "v1"
app = Flask(__name__)
CORS(app)
models_bp = Blueprint("models", __name__, url_prefix=f"/api/{API_VERSION}/models")
models_bp.register_blueprint(health_controller.bp)
models_bp.register_blueprint(predictions_controller.bp)
app.register_blueprint(models_bp)


def lambda_handler(event, context):
    print("EVENT", event)
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    app.run(debug=True)
