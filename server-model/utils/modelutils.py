import os
from typing import Dict, Any

import cv2
import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import (
    Conv3D,
    LSTM,
    Dense,
    Dropout,
    Bidirectional,
    MaxPool3D,
    Activation,
    Flatten,
    TimeDistributed,
    Input,
)

LIP_WIDTH = 112
LIP_HEIGHT = 80
TOTAL_FRAMES = 44

VOCAB = [x for x in "abdefgijklmnoprstuchy "]  # FONEMAS
CHANNELS = 1
CHAR_TO_NUM = tf.keras.layers.StringLookup(vocabulary=VOCAB, oov_token="")
NUM_TO_CHAR = tf.keras.layers.StringLookup(
    vocabulary=CHAR_TO_NUM.get_vocabulary(), oov_token="", invert=True
)
VOCABULARY_SIZE = CHAR_TO_NUM.vocabulary_size()


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


def get_cmodel_2110():
    model = tf.keras.models.load_model("./model/cmodel_x19_todos_2110.h5")
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


def get_cmodel_2110_v2():
    model = tf.keras.models.load_model("./model/cmodel_x19_todos_2110_v2.h5")
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


def get_cmodel_2310():
    model = tf.keras.models.load_model("./model/cmodel_x19_todos_2310_menosmati.h5")
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


def get_cmodel_2510():
    model = tf.keras.models.load_model(
        "./model/2510_todos_desde0_con_finetunning_todos.h5"
    )
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


def get_cmodel_2810():
    model = tf.keras.models.load_model("./model/2810_todos_desde0_sin_finetunning.h5")
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


def get_cmodel_2910():
    model = tf.keras.models.load_model(
        "./model/2910_todos_desde0_con_finetunning_todos.h5"
    )
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


def get_lipnet_model():
    model = Sequential()
    model.add(Input(shape=(44, LIP_HEIGHT, LIP_WIDTH, CHANNELS)))
    model.add(Conv3D(128, 3, padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPool3D((1, 2, 2)))

    model.add(Conv3D(256, 3, padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPool3D((1, 2, 2)))

    model.add(Conv3D(75, 3, padding="same"))
    model.add(Activation("relu"))
    model.add(MaxPool3D((1, 2, 2)))
    model.add(TimeDistributed(Flatten()))

    model.add(
        Bidirectional(
            LSTM(128, return_sequences=True, recurrent_initializer="glorot_uniform")
        )
    )
    model.add(Dropout(0.5))

    model.add(
        Bidirectional(
            LSTM(128, return_sequences=True, recurrent_initializer="glorot_uniform")
        )
    )
    model.add(Dropout(0.5))

    model.add(Dense(VOCABULARY_SIZE + 1, activation="softmax"))
    model.load_weights(os.path.join("model", "chkpoint_lipnet_2-10-2024-23-00.keras"))
    return model


MODELS = {
    "CMODEL": get_cmodel(),
    "CMODEL_2509": get_cmodel_2509(),
    "CMODEL_2110": get_cmodel_2110(),
    "CMODEL_2110_V2": get_cmodel_2110_v2(),
    "CMODEL_2310": get_cmodel_2310(),
    "CMODEL_2510": get_cmodel_2510(),
    "CMODEL_2810": get_cmodel_2810(),
    "CMODEL_2910": get_cmodel_2910(),
}

VALID_MODELS = [
    "CMODEL",
    "CMODEL_2509",
    "CMODEL_2110",
    "CMODEL_2110_V2",
    "CMODEL_2310",
    "CMODEL_2510",
    "CMODEL_2810",
    "CMODEL_2910",
]


def load_model(model: str = "CMODEL"):
    model = model.upper()
    with tf.device("/cpu:0"):
        if model not in VALID_MODELS:
            raise Exception(f"The model {model} does not exist")
        return MODELS[model]


# def translate_prediction(prediction, label_dict: Dict[str, Any]):
#     prob_per_class = []

#     maxLabel = ""
#     maxProb = 0.0

#     for i in range(len(prediction[0])):
#         prob_per_class.append((prediction[0][i], label_dict[i]))
#     sorted_probs = sorted(prob_per_class, key=lambda x: x[0], reverse=True)
#     for prob, label in sorted_probs:
#         print(f"{label}: {prob:.3f}")
#         if prob > maxProb:
#             maxProb = prob
#             maxLabel = label
#     return {"label": maxLabel, "probability": str(maxProb)}


def translate_prediction(prediction, label_dict: Dict[str, Any]):
    # Convert prediction to a NumPy array for efficient processing
    probs = np.array(prediction[0])

    # Get the indices of the sorted probabilities in descending order
    sorted_indices = np.argsort(-probs)  # Negative for descending order

    # Get the top probabilities and their corresponding labels
    sorted_probs = probs[sorted_indices]
    sorted_labels = [label_dict[i] for i in sorted_indices]

    # Print probabilities
    for prob, label in zip(sorted_probs, sorted_labels):
        print(f"{label}: {prob:.3f}")

    # Get the maximum probability and corresponding label
    max_index = np.argmax(sorted_probs)
    max_prob = sorted_probs[max_index]
    max_label = sorted_labels[max_index]
    return {"label": max_label, "probability": str(max_prob)}


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


def lipnet_preprocess_frame(lip_frame):

    return lip_frame


def process_frames(lip_frames):
    processed_frames = []
    for lip_frame in lip_frames:
        lip_frame = np.array(lip_frame)
        # TODO: Analyze if this blockcode is necessary
        # lip_frame = cv2.resize(lip_frame, (LIP_WIDTH, LIP_HEIGHT))
        # print("EXECUTING cv2.cvtColor")
        # lip_frame_lab = cv2.cvtColor(lip_frame, cv2.COLOR_BGR2LAB)
        # print("EXECUTING cv2.createCLAHE")
        # # Apply contrast stretching to the L channel of the LAB image
        # l_channel, a_channel, b_channel = cv2.split(lip_frame_lab)
        # clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(3, 3))
        # l_channel_eq = clahe.apply(l_channel)

        # # Merge the equalized L channel with the original A and B channels
        # lip_frame_eq = cv2.merge((l_channel_eq, a_channel, b_channel))
        # lip_frame_eq = cv2.cvtColor(lip_frame_eq, cv2.COLOR_LAB2BGR)
        image_8bit = (lip_frame * 255).astype("uint8")
        lip_frame_eq = cv2.GaussianBlur(image_8bit, (7, 7), 0)
        lip_frame_eq = cv2.bilateralFilter(lip_frame_eq, 5, 75, 75)
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # Apply the kernel to the input image
        lip_frame_eq = cv2.filter2D(lip_frame_eq, -1, kernel)
        image_8bit = (lip_frame_eq * 255).astype("uint8")
        lip_frame_eq = cv2.GaussianBlur(image_8bit, (5, 5), 0)
        # print("Executing cv2.cvtColor")
        # lip_frame_eq = cv2.cvtColor(lip_frame_eq, cv2.COLOR_BGR2GRAY)
        lip_frame_eq = np.expand_dims(lip_frame_eq, axis=-1)
        lip_frame = lip_frame_eq
        processed_frames.append(lip_frame_eq)
    frames_array = np.array(processed_frames, dtype=np.float32)

    # Padding or truncating frames to match TOTAL_FRAMES
    num_frames = frames_array.shape[0]
    if num_frames < TOTAL_FRAMES:
        padding = np.zeros(
            (TOTAL_FRAMES - num_frames, LIP_HEIGHT, LIP_WIDTH, CHANNELS),
            dtype=np.float32,
        )
        frames_array = np.concatenate([frames_array, padding], axis=0)
    elif num_frames > TOTAL_FRAMES:
        frames_array = frames_array[:TOTAL_FRAMES]

    mean = np.mean(frames_array)
    std = np.std(frames_array)
    normalized_frames = (frames_array - mean) / std

    return normalized_frames


def CTCLoss(y_true, y_pred):
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    loss = tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss
