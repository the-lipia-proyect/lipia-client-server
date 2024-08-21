import os
from typing import Dict, Any

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


MODELS = {"CMODEL": get_cmodel(), "CMODEL_RGB": get_cmodel_rgb()}

VALID_MODELS = ["CMODEL", "CMODEL_RGB"]


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
