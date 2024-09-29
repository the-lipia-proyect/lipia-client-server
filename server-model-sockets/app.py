import os
from flask import Flask, Blueprint

from flask_cors import CORS
import awsgi
from controllers import health_controller, predictions_controller

from utils.sockets_helper import socketio

API_VERSION = "v1"
app = Flask(__name__)
CORS(app)
socketio.init_app(app, path=f"socket.io/api/{API_VERSION}/models")


def lambda_handler(event, context):
    print("EVENT", event)
    return awsgi.response(app, event, context)


def print_routes(app):
    for rule in app.url_map.iter_rules():
        methods = ",".join(rule.methods)
        print(f"Endpoint: {rule.endpoint}, Path: {rule.rule}, Methods: {methods}")


if __name__ == "__main__":
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    socketio.run(app, debug=True, host="0.0.0.0", port=5000, log_output=True)
