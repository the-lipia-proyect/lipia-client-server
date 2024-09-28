import os
from typing import Dict, Any
import cv2
import tensorflow as tf
import numpy as np

LIP_WIDTH = 112
LIP_HEIGHT = 80


def get_cmodel():
    model = tf.keras.models.load_model("./model/cmodel_byn_x19_x120_20_08_api.h5")
    return model, {
        0: "adriano",
        1: "bueno",
        2: "chau",
        3: "como",
        4: "es",
        5: "estas",
        6: "esto",
        7: "ezequiel",
        8: "gabriel",
        9: "hola",
        10: "matias",
        11: "prueba",
        12: "rodrigo",
        13: "sil",
        14: "sos",
        15: "soy",
        16: "una",
        17: "vos",
        18: "yo",
    }


def get_cmodel_rgb():
    model = tf.keras.models.load_model("./model/cmodel_p1_p2_1707_2003.h5")
    return model, {
        0: "adriano",
        1: "bueno",
        2: "chau",
        3: "como",
        4: "es",
        5: "estas",
        6: "esto",
        7: "ezequiel",
        8: "gabriel",
        9: "hola",
        10: "matias",
        11: "prueba",
        12: "rodrigo",
        13: "sil",
        14: "sos",
        15: "soy",
        16: "una",
        17: "vos",
        18: "yo",
    }


def get_cmodel_2509():
    model = tf.keras.models.load_model("./model/cmodel_x19_full_2509_2035.h5")
    return model, {
        0: "adriano",
        1: "bueno",
        2: "chau",
        3: "como",
        4: "es",
        5: "estas",
        6: "esto",
        7: "ezequiel",
        8: "gabriel",
        9: "hola",
        10: "matias",
        11: "prueba",
        12: "rodrigo",
        13: "sil",
        14: "sos",
        15: "soy",
        16: "una",
        17: "vos",
        18: "yo",
    }


MODELS = {
    "CMODEL": get_cmodel(),
    "CMODEL_RGB": get_cmodel_rgb(),
    "CMODEL_2509": get_cmodel_2509(),
}

VALID_MODELS = ["CMODEL", "CMODEL_RGB", "CMODEL_2509"]


def load_model(model: str = "CMODEL_RGB"):
    model = model.upper()
    with tf.device("/cpu:0"):
        if model not in VALID_MODELS:
            raise Exception(f"The model {model} does not exist")
        return MODELS[model]


def translate_prediction(prediction, label_dict: Dict[str, Any]):
    prob_per_class = []

    maxLabel = ""
    maxProb = 0.0

    for i in range(len(prediction[0])):
        prob_per_class.append((prediction[0][i], label_dict[i]))
    sorted_probs = sorted(prob_per_class, key=lambda x: x[0], reverse=True)
    for prob, label in sorted_probs:
        print(f"{label}: {prob:.3f}")
        if prob > maxProb:
            maxProb = prob
            maxLabel = label
    return {"label": maxLabel, "probability": str(maxProb)}


def preprocess_frame(lip_frame):
    # Verificar si la imagen es RGB (3 canales) y convertirla a escala de grises
    if len(lip_frame.shape) == 3 and lip_frame.shape[-1] == 3:  # Imagen RGB
        lip_frame = cv2.cvtColor(lip_frame, cv2.COLOR_BGR2GRAY)

    # Redimensionar la imagen a las dimensiones requeridas
    lip_frame = cv2.resize(lip_frame, (LIP_WIDTH, LIP_HEIGHT))

    # Asegurarse de que la imagen es del tipo uint8 para aplicar CLAHE
    if lip_frame.dtype != np.uint8:
        lip_frame = lip_frame.astype(np.uint8)

    # Aplicar CLAHE para mejorar el contraste
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(3, 3))
    lip_frame_eq = clahe.apply(lip_frame)

    # Aplicar GaussianBlur y filtros adicionales
    lip_frame_eq = cv2.GaussianBlur(lip_frame_eq, (7, 7), 0)
    lip_frame_eq = cv2.bilateralFilter(lip_frame_eq, 5, 75, 75)

    # Aplicar un filtro de agudizado (sharpening)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    lip_frame_eq = cv2.filter2D(lip_frame_eq, -1, kernel)

    # Aplicar un desenfoque Gaussiano al final
    lip_frame_eq = cv2.GaussianBlur(lip_frame_eq, (5, 5), 0)

    return lip_frame_eq