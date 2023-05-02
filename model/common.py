import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from constants import DATASET_PATH_AFFIX, SEED, TEST_SIZE_PROPORTION
from numpy import typing as npt
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline

# change to DEBUG to see more logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s,%(lineno)d:%(message)s", stream=sys.stdout)


def measure_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.debug("Started at %s", datetime.now())

        result = func(*args, **kwargs)

        end_time = time.time()
        logging.debug("Ended at %s", datetime.now())
        logging.info("Execution time of %s: %.4f seconds", func.__name__, (end_time - start_time))

        return result

    return wrapper


def load_csv_to_predict(filepath: str) -> npt.NDArray[np.float64]:
    return np.loadtxt(
        filepath,
        skiprows=1,
        delimiter=",",
        encoding="utf-8",
    )


def load_csv_to_dataframe(filename: str = "combined.csv", nrows: int | None = 40_001) -> pd.DataFrame:
    # known duplicates from code, check
    # https://gitlab.com/hieulw/cicflowmeter/blob/8987fd239fb591f61049023432a9d43f97324ea0/src/cicflowmeter/flow.py#L190-L197
    columns_to_remove = [
        "Fwd Header Length.1",
        "Avg Fwd Segment Size",
        "Avg Bwd Segment Size",
        "CWE Flag Count",
        "Subflow Fwd Packets",
        "Subflow Fwd Bytes",
        "Subflow Bwd Packets",
        "Subflow Bwd Bytes",
    ]
    path = Path(os.environ["HOME"]) / "Downloads" / DATASET_PATH_AFFIX
    dataset = path / filename

    dataframe = pd.read_csv(
        dataset,
        compression=None,
        encoding="utf-8",
        delimiter=",",
        nrows=nrows,
        converters={78: label_to_float},
    )

    dataframe.rename(columns=lambda s: s.strip(), inplace=True)

    dataframe.drop(columns=columns_to_remove, inplace=True)

    # convert infinities to NaNs to remove them in one operation
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe.dropna(how="any", inplace=True)

    return dataframe


def split_dataset(
    dataset: pd.DataFrame, rand_state: int | None = SEED, test_size: float = TEST_SIZE_PROPORTION
) -> list[pd.DataFrame | pd.Series]:
    features, targets = dataset_to_x_and_y(dataset)

    logging.debug("Data shape before split is %s", dataset.shape)
    logging.debug("Random seed is %s", rand_state)
    logging.debug("Test size is %.2f percent of dataset", test_size * 100)

    return train_test_split(
        features,
        targets,
        test_size=test_size,
        # https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-with-stratification-based-on-class-labels
        stratify=targets,
        random_state=rand_state,
    )


def cross_validator(model: Pipeline, dataset: pd.DataFrame) -> npt.NDArray[np.float64]:
    features, targets = dataset_to_x_and_y(dataset)
    folds = 5

    logging.debug("Cross validating with %d folds", folds)
    return cross_val_score(model, X=features, y=targets, cv=folds, scoring='f1', verbose=1)


def filename_for_archiving(prefix: str | None) -> str:
    suffix = f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}.skops'

    if prefix is None:
        return "model" + suffix
    return prefix + suffix


def label_to_float(label: str) -> float:
    if label == "BENIGN":
        return 0.0
    return 1.0


def float_to_label(prediction: float) -> str:
    if prediction == 0.0:
        return "BENIGN"
    return "MALICIOUS"


def dataset_to_x_and_y(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    return dataset.drop(columns="Label", inplace=False), dataset["Label"]
