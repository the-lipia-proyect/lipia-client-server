# import base64
# import os
import json
import gzip
from flask import Flask, request, jsonify, Blueprint
import numpy as np

from utils.modelutils import load_model, translate_prediction
from flask_cors import CORS, cross_origin
import awsgi


API_VERSION = "v1"
app = Flask(__name__)
CORS(app)
models_bp = Blueprint("models", __name__, url_prefix=f"/api/{API_VERSION}/models")


@models_bp.route("/health", methods=["GET"])
def health():
    response = {"message": "Healthy"}
    return jsonify(response), 200


@models_bp.route("/predictions", methods=["POST"])
def predictions():
    try:
        compressed_data = request.data
        decompressed_data = gzip.decompress(compressed_data)

        # Parse the JSON from the decompressed data
        payload = json.loads(decompressed_data)
        # payload = request.get_json()
        model_to_execute = payload.get("model", "CMODEL_RGB")
        encoded_frames = payload.get("frames", None)
        with_rgb = payload.get("with_rgb", False)
        if encoded_frames is None:
            return (
                jsonify({"message": "Invalid Body: the key body.frames is missing"}),
                400,
            )
        frames = encoded_frames
        model, label_dict = load_model(model_to_execute)
        if model == None:
            return (
                jsonify({"message": "Error loading the model"}),
                500,
            )
        loaded_data = np.array(frames).reshape((-1, 44, 80, 112, 3 if with_rgb else 1))

        prediction = model.predict(loaded_data)
        translated_prediction = translate_prediction(prediction, label_dict)
        return jsonify({"prediction": translated_prediction}), 200
    except Exception as e:
        print("ERROR", e)
        return {"message": str(e)}, 500


app.register_blueprint(models_bp)


def lambda_handler(event, context):
    return awsgi.response(app, event, context)


if __name__ == "__main__":
    app.run(debug=True)
