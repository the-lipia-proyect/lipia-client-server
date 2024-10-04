import base64
import gzip
import json

from flask_injector import inject
import numpy as np

from utils.responses_helper import ok, internal_server_error, bad_request
from .interfaces.predictions_service import IPredictionsService
from dtos.get_prediction_response_dto import GetPredictionResponseDto
from dtos.get_prediction_request_dto import GetPredictionRequestDto
from dtos.get_prediction_compressed_request_dto import GetPredictionCompressedRequestDto
from utils.modelutils import load_model, preprocess_frame, translate_prediction


class PredictionsService(IPredictionsService):
    @inject
    def __init__(self):
        pass

    def predict(self, req: GetPredictionRequestDto) -> GetPredictionResponseDto:

        model_to_execute = req.model
        encoded_frames = req.frames
        with_rgb = req.with_rgb
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
        response = GetPredictionResponseDto(prediction=translated_prediction)
        return ok(response)

    def predict_opencv(self, req: GetPredictionRequestDto) -> GetPredictionResponseDto:
        model_to_execute = req.model
        encoded_frames = req.frames
        with_rgb = req.with_rgb
        if encoded_frames is None:
            return bad_request(
                {"message": "Invalid Body: the key body.frames is missing"}
            )
        frames = encoded_frames

        model, label_dict = load_model(model_to_execute)

        if model is None:
            return internal_server_error({"message": "Error loading the model"})

        # Directorio donde guardarás las imágenes usando pathlib
        # save_dir = Path("./saved_frames")
        # save_dir.mkdir(parents=True, exist_ok=True)  # Crea el directorio si no existe

        # Preprocesar cada frame antes de la predicción
        preprocessed_frames = []
        for idx, frame in enumerate(frames):
            # Asegurarse de que cada frame es un numpy array
            if not isinstance(frame, np.ndarray):
                frame = np.array(frame)

            # Preprocesar el frame (convertir a escala de grises si es RGB)
            preprocessed_frame = preprocess_frame(frame)

            preprocessed_frames.append(preprocessed_frame)

            # # Guardar algunos frames en el directorio antes de la predicción
            # if idx < 5:  # Por ejemplo, guardar los primeros 5 frames
            #     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            #     filename = f"frame_{idx}_{timestamp}.png"
            #     file_path = save_dir / filename  # Crear la ruta del archivo
            #     cv2.imwrite(str(file_path), preprocessed_frame)  # Guardar la imagen

        # Asegúrate de que los datos están en la forma correcta para el modelo
        loaded_data = np.array(preprocessed_frames).reshape(
            (-1, 44, 80, 112, 1)
        )  # Siempre 1 canal para escala de grises

        prediction = model.predict(loaded_data)
        translated_prediction = translate_prediction(prediction, label_dict)
        response = GetPredictionResponseDto(prediction=translated_prediction)
        return ok(response)

    def predict_compressed(
        self, req: GetPredictionCompressedRequestDto
    ) -> GetPredictionResponseDto:
        # Decode the Base64 encoded data
        encoded_data = req.data
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
        response = GetPredictionResponseDto(prediction=translated_prediction)
        return ok(response)

    def predict_compressed_opencv(
        self, req: GetPredictionCompressedRequestDto
    ) -> GetPredictionResponseDto:
        # Decode the Base64 encoded data
        encoded_data = req.data
        if not encoded_data:
            return bad_request({"message": "No data provided"})

        compressed_data = base64.b64decode(encoded_data)

        # Decompress the gzipped data
        decompressed_data = gzip.decompress(compressed_data)

        # Parse the JSON from the decompressed data
        payload = json.loads(decompressed_data)
        model_to_execute = payload.get("model", "CMODEL")
        encoded_frames = payload.get("frames", None)
        with_rgb = payload.get("with_rgb", False)

        if encoded_frames is None:
            return bad_request({"message": "Invalid Body: the key frames is missing"})

        frames = encoded_frames
        model, label_dict = load_model(model_to_execute)

        if model is None:
            return internal_server_error({"message": "Error loading the model"})

        # Directorio donde guardarás las imágenes usando pathlib
        # save_dir = Path("./saved_frames")
        # save_dir.mkdir(parents=True, exist_ok=True)  # Crea el directorio si no existe

        # Preprocesar cada frame antes de la predicción
        preprocessed_frames = []
        for idx, frame in enumerate(frames):
            # Asegurarse de que cada frame es un numpy array
            if not isinstance(frame, np.ndarray):
                frame = np.array(frame)

            # Preprocesar el frame (convertir a escala de grises si es RGB)
            preprocessed_frame = preprocess_frame(frame)

            preprocessed_frames.append(preprocessed_frame)

            # # Guardar algunos frames en el directorio antes de la predicción
            # if idx < 5:  # Por ejemplo, guardar los primeros 5 frames
            #     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            #     filename = f"frame_{idx}_{timestamp}.png"
            #     file_path = save_dir / filename  # Crear la ruta del archivo
            #     cv2.imwrite(str(file_path), preprocessed_frame)  # Guardar la imagen

        # Asegúrate de que los datos están en la forma correcta para el modelo
        loaded_data = np.array(preprocessed_frames).reshape(
            (-1, 44, 80, 112, 1)
        )  # Siempre 1 canal para escala de grises

        prediction = model.predict(loaded_data)
        translated_prediction = translate_prediction(prediction, label_dict)
        response = GetPredictionResponseDto(prediction=translated_prediction)
        return ok(response)
