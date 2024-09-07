import os

from flask import Flask, Blueprint
from flask_cors import CORS
import awsgi
from dotenv import load_dotenv
from flask_cognito import CognitoAuth
from flask_injector import FlaskInjector

from services.dependency_injector import configure_di
from controllers import (
    health_controller,
    voices_controller,
    auth_controller,
    user_controller,
    user_configurations_controller,
    shortcuts_controller,
    interpretations_controller,
    files_controller,
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
cognito = CognitoAuth(app)

management_bp = Blueprint(
    "management", __name__, url_prefix=f"/api/{API_VERSION}/management"
)
management_bp.register_blueprint(health_controller.bp)
management_bp.register_blueprint(voices_controller.bp)
management_bp.register_blueprint(auth_controller.bp)
management_bp.register_blueprint(user_controller.bp)
management_bp.register_blueprint(user_configurations_controller.bp)
management_bp.register_blueprint(shortcuts_controller.bp)
management_bp.register_blueprint(interpretations_controller.bp)
management_bp.register_blueprint(files_controller.bp)
app.register_blueprint(management_bp)
FlaskInjector(app=app, modules=[configure_di])


def lambda_handler(event, context):
    print("EVENT", event)
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run(debug=True)
