from flask import Blueprint, jsonify, request, Response, stream_with_context
import base64
import http
import json
import gzip
import numpy as np
from utils.responses_helper import ok, bad_request, internal_server_error
from utils.modelutils import load_model, translate_prediction

bp = Blueprint("predictions", __name__, url_prefix="/predictions")


@bp.route(None, methods=[http.HTTPMethod.POST])
def post_predictions():
    try:
        payload = request.get_json()
        model_to_execute = payload.get("model", "CMODEL_RGB")
        encoded_frames = payload.get("frames", None)
        with_rgb = payload.get("with_rgb", False)
        if encoded_frames is None:
            return bad_request(
                {"message": "Invalid Body: the key body.frames is missing"}
            )
        frames = encoded_frames
        model, label_dict = load_model(model_to_execute)
        if model == None:
            return internal_server_error({"message": "Error loading the model"})
        loaded_data = np.array(frames).reshape((-1, 44, 80, 112, 3 if with_rgb else 1))

        prediction = model.predict(loaded_data)
        translated_prediction = translate_prediction(prediction, label_dict)
        return ok({"prediction": translated_prediction})
    except Exception as e:
        print("ERROR", e)
        return internal_server_error({"message": str(e)})


@bp.route("/compressed", methods=[http.HTTPMethod.POST])
def post_predictions_compressed():
    try:
        # Decode the Base64 encoded data
        encoded_data = request.json.get("data", None)
        if not encoded_data:
            return bad_request({"message": "No data provided"})

        compressed_data = base64.b64decode(encoded_data)

        # Decompress the gzipped data
        decompressed_data = gzip.decompress(compressed_data)

        # Parse the JSON from the decompressed data
        payload = json.loads(decompressed_data)
        model_to_execute = payload.get("model", "CMODEL_RGB")
        encoded_frames = payload.get("frames", None)
        with_rgb = payload.get("with_rgb", False)

        if encoded_frames is None:
            return bad_request({"message": "Invalid Body: the key frames is missing"})

        frames = encoded_frames
        model, label_dict = load_model(model_to_execute)

        if model is None:
            return internal_server_error({"message": "Error loading the model"})

        loaded_data = np.array(frames).reshape((-1, 44, 80, 112, 3 if with_rgb else 1))
        prediction = model.predict(loaded_data)
        translated_prediction = translate_prediction(prediction, label_dict)

        return ok({"prediction": translated_prediction})

    except Exception as e:
        print("ERROR", e)
        return internal_server_error({"message": str(e)})


@bp.route("/stream", methods=[http.HTTPMethod.POST])
def post_predictions_stream():
    try:

        def generate_predictions():
            for chunk in request.iter_content(chunk_size=4096):
                if chunk:
                    try:
                        # Decodifica y descomprime cada chunk
                        compressed_data = base64.b64decode(chunk)
                        decompressed_data = gzip.decompress(compressed_data)
                        payload = json.loads(decompressed_data)

                        model_to_execute = payload.get("model", "CMODEL_RGB")
                        encoded_frames = payload.get("frames", None)
                        with_rgb = payload.get("with_rgb", False)

                        if encoded_frames is None:
                            yield jsonify(
                                {"message": "Invalid Body: the key frames is missing"}
                            ), 400
                            return

                        frames = encoded_frames
                        model, label_dict = load_model(model_to_execute)
                        if model is None:
                            yield jsonify({"message": "Error loading the model"}), 500
                            return

                        loaded_data = np.array(frames).reshape(
                            (-1, 44, 80, 112, 3 if with_rgb else 1)
                        )
                        prediction = model.predict(loaded_data)
                        translated_prediction = translate_prediction(
                            prediction, label_dict
                        )

                        yield jsonify({"prediction": translated_prediction}), 200

                    except Exception as e:
                        print("ERROR", e)
                        yield jsonify({"message": str(e)}), 500
                        return

        return Response(
            stream_with_context(generate_predictions()), content_type="application/json"
        )

    except Exception as e:
        print("ERROR", e)
        return internal_server_error({"message": str(e)})
