"""
=========================================
Module : model.py
Project: KOTTU
Purpose: LSTM Model Architecture
=========================================
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


class KOTTUModel:

    def build_model(self, input_shape, num_classes):

        model = Sequential()

        model.add(
            LSTM(
                64,
                input_shape=input_shape,
                return_sequences=True
            )
        )

        model.add(Dropout(0.3))

        model.add(LSTM(32))

        model.add(Dropout(0.3))

        model.add(Dense(64, activation="relu"))

        model.add(Dense(num_classes, activation="softmax"))

        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

        return model