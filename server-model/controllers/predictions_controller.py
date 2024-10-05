import http
import json

from flask import Blueprint, request, Response, stream_with_context
from flask_injector import inject
from flask_cognito import cognito_auth_required
from pydantic import ValidationError

from services.interfaces.predictions_service import IPredictionsService
from utils.responses_helper import ok, bad_request, internal_server_error
from dtos.get_prediction_request_dto import GetPredictionRequestDto
from dtos.get_prediction_compressed_request_dto import GetPredictionCompressedRequestDto
from dtos.get_lipnet_prediction_request_dto import GetLipnetPredictionRequestDto

bp = Blueprint("predictions", __name__, url_prefix="/predictions")


@bp.route(None, methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_predictions(predictions_service: IPredictionsService):
    try:
        req = GetPredictionRequestDto(**request.get_json())
        return predictions_service.predict(req)
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        print("Error:", e)
        return internal_server_error({"message": str(e)})


@bp.route("/compressed", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_predictions_compressed(predictions_service: IPredictionsService):
    try:
        req = GetPredictionCompressedRequestDto(**request.get_json())
        return predictions_service.predict_compressed(req)
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        print("Error:", e)
        return internal_server_error({"message": str(e)})


@bp.route("/opencv", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_predictions_opencv(predictions_service: IPredictionsService):
    try:
        req = GetPredictionRequestDto(**request.get_json())
        return predictions_service.predict_opencv(req)
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        print("Error:", e)
        return internal_server_error({"message": str(e)})


@bp.route("/compressed/opencv", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_predictions_compressed_opencv(predictions_service: IPredictionsService):
    try:
        req = GetPredictionCompressedRequestDto(**request.get_json())
        return predictions_service.predict_compressed_opencv(req)
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        print("Error:", e)
        return internal_server_error({"message": str(e)})


@bp.route("/lipnet", methods=[http.HTTPMethod.POST])
@cognito_auth_required
@inject
def post_predictions_lipnet(predictions_service: IPredictionsService):
    try:
        req = GetLipnetPredictionRequestDto(**request.get_json())
        return predictions_service.predict_lipnet(req)
    except ValidationError as e:
        return bad_request({"message": json.loads(e.json())})
    except Exception as e:
        print("Error:", e)
        return internal_server_error({"message": str(e)})


# TODO: Analyze if this endpoint is necessary
# @bp.route("/stream", methods=[http.HTTPMethod.POST])
# @cognito_auth_required
# @inject
# def post_predictions_stream(predictions_service: IPredictionsService):
#     try:

#         def generate_predictions():
#             for chunk in request.iter_content(chunk_size=4096):
#                 if chunk:
#                     try:
#                         # Decodifica y descomprime cada chunk
#                         compressed_data = base64.b64decode(chunk)
#                         decompressed_data = gzip.decompress(compressed_data)
#                         payload = json.loads(decompressed_data)

#                         model_to_execute = payload.get("model", "CMODEL_RGB")
#                         encoded_frames = payload.get("frames", None)
#                         with_rgb = payload.get("with_rgb", False)

#                         if encoded_frames is None:
#                             yield jsonify(
#                                 {"message": "Invalid Body: the key frames is missing"}
#                             ), 400
#                             return

#                         frames = encoded_frames
#                         model, label_dict = load_model(model_to_execute)
#                         if model is None:
#                             yield jsonify({"message": "Error loading the model"}), 500
#                             return

#                         loaded_data = np.array(frames).reshape(
#                             (-1, 44, 80, 112, 3 if with_rgb else 1)
#                         )
#                         prediction = model.predict(loaded_data)
#                         translated_prediction = translate_prediction(
#                             prediction, label_dict
#                         )

#                         yield jsonify({"prediction": translated_prediction}), 200

#                     except Exception as e:
#                         print("ERROR", e)
#                         yield jsonify({"message": str(e)}), 500
#                         return

#         return Response(
#             stream_with_context(generate_predictions()), content_type="application/json"
#         )

#     except Exception as e:
#         print("ERROR", e)
#         return internal_server_error({"message": str(e)})
