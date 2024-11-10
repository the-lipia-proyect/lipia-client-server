import os
from flask import Flask, Blueprint

from flask_cors import CORS
from flask_cognito import CognitoAuth
import awsgi
from dotenv import load_dotenv
from flask_injector import FlaskInjector

from services.dependency_injector import configure_di
from controllers import (
    health_controller,
    predictions_controller,
    available_models_controller,
)

load_dotenv()

API_VERSION = "v1"
app = Flask(__name__)
app.config.update(
    {
        "COGNITO_REGION": os.getenv("AWS_REGION", "us-east-1"),
        "COGNITO_USERPOOL_ID": os.getenv("AWS_COGNITO_USERS_POOL_ID"),
        # optional
        "COGNITO_APP_CLIENT_ID": os.getenv(
            "AWS_COGNITO_USERS_CLIENT_ID"
        ),  # client ID you wish to verify user is authenticated against
        "COGNITO_CHECK_TOKEN_EXPIRATION": False,  # disable token expiration checking for testing purposes
        "COGNITO_JWT_HEADER_NAME": "Authorization",
        "COGNITO_JWT_HEADER_PREFIX": "Bearer",
    }
)
CORS(app)

# cognito = CognitoAuth(app)
models_bp = Blueprint("models", __name__, url_prefix=f"/api/{API_VERSION}/models")
models_bp.register_blueprint(health_controller.bp)
models_bp.register_blueprint(predictions_controller.bp)
models_bp.register_blueprint(available_models_controller.bp)
app.register_blueprint(models_bp)
FlaskInjector(app=app, modules=[configure_di])


def lambda_handler(event, context):
    print("EVENT", event)
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    app.run(debug=True)
