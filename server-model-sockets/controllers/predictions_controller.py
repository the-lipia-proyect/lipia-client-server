from flask import Blueprint, jsonify, request, Response, stream_with_context
import io
import base64
import http
import json
import gzip
import numpy as np
from utils.responses_helper import ok, bad_request, internal_server_error
from utils.modelutils import load_model, translate_prediction

from utils.sockets_helper import socketio, Namespace
from flask_socketio import emit


NAMESPACE = "/predictions"


class PredictionsController(Namespace):
    def on_connect(self):
        """Handle client connection."""
        print("PASA POR EL CONNECT")

    def on_prediction(self, data):
        """Handle prediction events."""
        print("Executing on_prediction handler", data)

        try:
            # Decode the Base64 encoded data
            encoded_data = json.loads(data).get("data", None)
            if not encoded_data:
                emit("prediction_response_error", {"message": "No data provided"})

            compressed_data = base64.b64decode(encoded_data)

            # Decompress the gzipped data
            decompressed_data = gzip.decompress(compressed_data)

            # Parse the JSON from the decompressed data
            payload = json.loads(decompressed_data)
            model_to_execute = payload.get("model", "CMODEL_RGB")
            encoded_frames = payload.get("frames", None)
            with_rgb = payload.get("with_rgb", False)

            if encoded_frames is None:
                emit(
                    "prediction_response_error",
                    {"message": "Invalid Body: the key frames is missing"},
                )

            frames = encoded_frames
            model, label_dict = load_model(model_to_execute)

            if model is None:
                emit(
                    "prediction_response_error",
                    {"message": "Error loading the model"},
                )

            loaded_data = np.array(frames).reshape(
                (-1, 44, 80, 112, 3 if with_rgb else 1)
            )
            prediction = model.predict(loaded_data)
            translated_prediction = translate_prediction(prediction, label_dict)
            emit("prediction_response", {"prediction": translated_prediction})

        except Exception as e:
            print("ERROR", e)
            emit("prediction_response_error", {"message": str(e)})


socketio.on_namespace(PredictionsController(NAMESPACE))


# def decode_and_decompress(base64_encoded_chunk):
#     """Decode Base64 and decompress GZIP data"""
#     # Decode Base64
#     compressed_data = base64.b64decode(base64_encoded_chunk)
#     # Decompress GZIP
#     with gzip.GzipFile(
#         fileobj=io.BytesIO(compressed_data), mode="rb"
#     ) as decompressed_file:
#         return decompressed_file.read()


# @socketio.on("stream")
# def handle_streamed_data(message):
#     try:
#         # Decode and decompress the incoming frame data
#         encoded_data = message.get("data", None)
#         if not encoded_data:
#             return

#         compressed_body = base64.b64decode(encoded_data)
#         decompressed_body = gzip.decompress(compressed_body).decode("utf-8")
#         payload = json.loads(decompressed_body)

#         frames = payload.get("frames")
#         model_to_execute = payload.get("model")
#         with_rgb = payload.get("with_rgb", False)

#         # Accumulate frames if necessary or process immediately
#         # Once 44 frames are received, process them with the model
#         # (You can accumulate frames on the server as needed)

#         # Assuming we've accumulated 44 frames
#         if len(frames) == 44:
#             model, label_dict = load_model(model_to_execute)
#             if model is None:
#                 emit("error", {"message": "Error loading the model"})
#                 return

#             # Reshape frames and make a prediction
#             loaded_data = np.array(frames).reshape(
#                 (-1, 44, 80, 112, 3 if with_rgb else 1)
#             )
#             prediction = model.predict(loaded_data)
#             translated_prediction = translate_prediction(prediction, label_dict)

#             emit("prediction", {"prediction": translated_prediction})
#     except Exception as e:
#         emit("error", {"message": str(e)})


# # @bp.route("/stream", methods=[http.HTTPMethod.POST])
# # def handle_streamed_data():
# #     full_data = b""
# #     frames_received = []
# #     frames_count = 44  # The expected number of frames to receive
# #     data = ""
# #     while True:
# #         chunk = request.stream.read(4096)
# #         if not chunk:
# #             break
# #         data += chunk.decode("utf-8")
# #     print("FRAME_DATA", data)
# #     # while len(frames_received) < frames_count:
# #     #     # Read frame by frame from the request stream
# #     #     frame_chunk = request.stream.read(5000000)  # Read a chunk of 4096 bytes
# #     #     if not frame_chunk:
# #     #         break  # Break the loop if no more data is coming

# #     #     # Assuming that each chunk corresponds to one frame (depending on your client)
# #     #     try:
# #     #         print("FRAME_CHUNK", frame_chunk)
# #     #         # Decode the incoming frame from bytes
# #     #         decoded_frame = json.loads(
# #     #             frame_chunk.decode("utf-8")
# #     #         )  # Modify the decoding based on the incoming frame format
# #     #         frames_received.append(decoded_frame["frames"])  # Collect the frame
# #     #     except json.JSONDecodeError as e:
# #     #         return f"Invalid JSON data: {e}", 400

# #     # Ensure we've received the expected number of frames
# #     # if len(frames_received) != frames_count:
# #     #     return bad_request({"message": "Not enough frames received"})

# #     # Once we have all the frames, process the data
# #     try:
# #         payload = json.loads(data)
# #         frames = payload.get(
# #             "frames"
# #         )  # These are the collected frames (without encoding or compressing)
# #         model_to_execute = payload.get("model")
# #         # model_to_execute = (
# #         #     "CMODEL_RGB"  # Hardcoding model for now, you can adjust this as needed
# #         # )
# #         with_rgb = payload.get("with_rgb")
# #         # with_rgb = False  # Hardcoding the RGB flag for now, adjust if needed

# #         # Load the model based on the selected one
# #         model, label_dict = load_model(model_to_execute)
# #         if model is None:
# #             return internal_server_error({"message": "Error loading the model"})

# #         # Reshape the data to match the input for the model
# #         loaded_data = np.array(frames).reshape((-1, 44, 80, 112, 3 if with_rgb else 1))

# #         # Make predictions
# #         prediction = model.predict(loaded_data)
# #         translated_prediction = translate_prediction(prediction, label_dict)

# #         return ok({"prediction": translated_prediction})
# #     except Exception as e:
# #         return f"Error during prediction: {e}", 500


# # @bp.route("/stream", methods=[http.HTTPMethod.POST])
# # def handle_streamed_data():
# #     full_data = b""
# #     while True:
# #         # Read chunk by chunk from the request stream
# #         base64_chunk = request.stream.read()
# #         if not base64_chunk:
# #             break

# #         # Decode and decompress the chunk
# #         decompressed_chunk = decode_and_decompress(base64_chunk)
# #         full_data += decompressed_chunk
# #         # full_data += base64_chunk

# #     # Process the full_data
# #     try:
# #         # decompressed_chunk = decode_and_decompress(base64_chunk)
# #         # payload = json.loads(decompressed_chunk)
# #         payload = json.loads(full_data)
# #         print("PAYLOAD", payload)
# #         model_to_execute = payload.get("model", "CMODEL_RGB")
# #         encoded_frames = payload.get("frames", None)
# #         with_rgb = payload.get("with_rgb", False)

# #         if encoded_frames is None:
# #             return bad_request({"message": "Invalid Body: the key frames is missing"})

# #         frames = encoded_frames
# #         model, label_dict = load_model(model_to_execute)

# #         if model is None:
# #             return internal_server_error({"message": "Error loading the model"})

# #         loaded_data = np.array(frames).reshape((-1, 44, 80, 112, 3 if with_rgb else 1))
# #         prediction = model.predict(loaded_data)
# #         translated_prediction = translate_prediction(prediction, label_dict)

# #         return ok({"prediction": translated_prediction})
# #         # Now you can use 'data' for prediction or other processing
# #         # Example: process_data(data)
# #     except json.JSONDecodeError as e:
# #         return f"Invalid JSON data: {e}", 400

# #     return "Data processed", 200


# # @bp.route("/stream", methods=[http.HTTPMethod.POST])
# # def post_predictions_stream():
# #     try:
# #         print("Request received for streaming")

# #         def generate_predictions():
# #             buffer = ""
# #             buffer = b""  # Buffer to store the complete compressed data
# #             while True:
# #                 # Read the stream in chunks
# #                 chunk = request.stream.read(4096)
# #                 if not chunk:
# #                     break  # Stop reading when no more chunks are left

# #                 # Accumulate the chunks into the buffer
# #                 buffer += chunk
# #             # print("BUFFER", buffer)
# #             try:
# #                 # Once all chunks are collected, decode and decompress the buffer
# #                 compressed_data = base64.b64decode(buffer)
# #                 print("COMPRESSED DATA", compressed_data)
# #                 decompressed_data = gzip.decompress(compressed_data)
# #                 print("DECOMPRESSED DATA", decompressed_data)
# #                 payload = json.loads(decompressed_data)
# #                 print("PAYLOAD", payload)
# #                 model_to_execute = payload.get("model", "CMODEL_RGB")
# #                 encoded_frames = payload.get("frames", None)
# #                 with_rgb = payload.get("with_rgb", False)

# #                 if encoded_frames is None:
# #                     yield json.dumps(
# #                         {"message": "Invalid Body: the key frames is missing"}
# #                     ).encode("utf-8"), 400
# #                     return

# #                 frames = encoded_frames
# #                 model, label_dict = load_model(model_to_execute)
# #                 if model is None:
# #                     yield json.dumps({"message": "Error loading the model"}).encode(
# #                         "utf-8"
# #                     ), 500
# #                     return

# #                 loaded_data = np.array(frames).reshape(
# #                     (-1, 44, 80, 112, 3 if with_rgb else 1)
# #                 )
# #                 prediction = model.predict(loaded_data)
# #                 translated_prediction = translate_prediction(prediction, label_dict)

# #                 yield json.dumps({"prediction": translated_prediction}).encode(
# #                     "utf-8"
# #                 ), 200

# #             except Exception as e:
# #                 print("ERROR IN GENERATE PREDICTIONS", e)
# #                 yield json.dumps({"message": str(e)}).encode("utf-8"), 500
# #                 return

# #         return Response(
# #             stream_with_context(generate_predictions()), content_type="application/json"
# #         )

# #     except Exception as e:
# #         print("ERROR", e)
# #         return internal_server_error({"message": str(e)})
