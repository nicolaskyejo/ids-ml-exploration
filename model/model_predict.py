import glob
import logging
import os
from typing import Any

import numpy as np
from common import float_to_label, load_csv_to_predict
from numpy import typing as npt
from skops.io import load


def open_saved_model(filename: str | None = None) -> Any:
    if filename is not None:
        logging.debug("Loading model %s", filename)
        return load(filename, trusted=True)

    pattern = "ids_*.skops"
    files = glob.glob(pattern)
    latest_model = max(files, key=os.path.getmtime)
    logging.debug("Loading model %s", latest_model)

    return load(
        latest_model,
        trusted=["numpy.float64", "numpy.int64", "sklearn.neural_network._stochastic_optimizers.AdamOptimizer"],
    )


def predict(model: Any, features: npt.NDArray[np.float64]) -> float:
    prediction_array: npt.NDArray[np.float64] = model.predict(features)
    return prediction_array.max()


def load_input_csv_and_predict(csv_to_predict: str, model_to_use: str | None = None) -> str:
    model = open_saved_model(model_to_use)
    data_to_predict = load_csv_to_predict(csv_to_predict)

    # if we only have a "row" to predict
    if data_to_predict.ndim == 1:
        data_to_predict = data_to_predict.reshape(1, -1)

    prediction = predict(model=model, features=data_to_predict)
    label = float_to_label(prediction)

    logging.info("Prediction of input data is that it is %s", label)
    return label


if __name__ == "__main__":
    print(load_input_csv_and_predict("in.csv"))
