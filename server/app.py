from flask import Flask, Blueprint
from flask_cors import CORS
import awsgi
from dotenv import load_dotenv

from controllers import health_controller, voices_controller

load_dotenv()
API_VERSION = "v1"
app = Flask(__name__)
CORS(app)
management_bp = Blueprint(
    "management", __name__, url_prefix=f"/api/{API_VERSION}/management"
)
management_bp.register_blueprint(health_controller.bp)
management_bp.register_blueprint(voices_controller.bp)
app.register_blueprint(management_bp)


def lambda_handler(event, context):
    print("EVENT", event)
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run(debug=True)
