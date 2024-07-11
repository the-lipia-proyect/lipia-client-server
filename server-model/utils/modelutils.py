import os

import tensorflow as tf
import numpy as np

LABEL_DICT = {0: "boludo", 1: "chau", 2: "hola", 3: "vos", 4: "yo"}
LIP_WIDTH = 112
LIP_HEIGHT = 80
def get_chino_model():
    model = tf.keras.models.load_model("./model/cmodel_01_07_2024.h5")
    return model

def get_old_chino_model():
    return None
    # input_shape = (22, 80, 112, 3)
    # model = tf.keras.Sequential(
    #     [
    #         tf.keras.layers.Conv3D(
    #             8,
    #             (3, 3, 3),
    #             activation="relu",
    #             input_shape=input_shape,
    #             kernel_regularizer=tf.keras.regularizers.l2(0.001),
    #         ),
    #         tf.keras.layers.MaxPooling3D((2, 2, 2)),
    #         tf.keras.layers.Conv3D(
    #             32, (3, 3, 3), activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.001)
    #         ),
    #         tf.keras.layers.MaxPooling3D((2, 2, 2)),
    #         tf.keras.layers.Conv3D(
    #             256, (3, 3, 3), activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.001)
    #         ),
    #         tf.keras.layers.Flatten(),
    #         tf.keras.layers.Dense(1024, activation="relu"),
    #         tf.keras.layers.Dropout(0.5),
    #         tf.keras.layers.Dense(256, activation="relu"),
    #         tf.keras.layers.Dropout(0.5),
    #         tf.keras.layers.Dense(64, activation="relu"),
    #         tf.keras.layers.Dropout(0.5),
    #         tf.keras.layers.Dense(
    #             5, activation="softmax"
    #         ),  # el valor 5 tiene qe coincidir con las clases que quiere adivinar
    #     ]
    # )

    # model.load_weights(
    #     "./model/checkpoint_5palabras_x21_v_y_h_ch_b.h5"
    # )
    # return model

MODELS = {
    "CHINO": get_chino_model(),
    "OLD_CHINO": get_old_chino_model()
}

VALID_MODELS = ["CHINO","OLD_CHINO"]
def load_model(model: str ="CHINO"):
    model = model.upper()
    with tf.device('/cpu:0'):
        if model not in VALID_MODELS:
            raise Exception(f"The model {model} does not exist")
        return MODELS[model]


def translate_prediction(prediction):
    prob_per_class = []

    maxLabel = ""
    maxProb = 0.0

    for i in range(len(prediction[0])):
        prob_per_class.append((prediction[0][i], LABEL_DICT[i]))
    sorted_probs = sorted(prob_per_class, key=lambda x: x[0], reverse=True)
    for prob, label in sorted_probs:
        print(f"{label}: {prob:.3f}")
        if prob > maxProb:
            maxProb = prob
            maxLabel = label
    return {
        "label": maxLabel,
        "probability": str(maxProb)
    }
