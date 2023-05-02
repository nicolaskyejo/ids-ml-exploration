import logging

import numpy as np
from common import cross_validator, load_csv_to_dataframe, measure_time
from constants import PART_OF_DATA, ALL_DATA
from k_nearest_neighbor import knn_model
from logistic_regression import lr_model
from mlp_neural_network import mlp_model
from random_forest import random_forest_model
from support_vector_machine import svm_model


@measure_time
def score_models() -> tuple[str, np.float64]:
    pandas_dataframe = load_csv_to_dataframe(ALL_DATA, nrows=None)
    models = [
        ("knn", knn_model()),
        ("logit", lr_model()),
        # ("svm", svm_model()),
        ("randforest", random_forest_model()),
        ("MLP", mlp_model()),
    ]
    models_mean_scores = []

    for name, model in models:
        scores = cross_validator(model, dataset=pandas_dataframe)
        logging.debug("%s scores -> %s", name, scores)

        mean_score = np.mean(scores) * 100
        models_mean_scores.append(mean_score)
        logging.info("Average score for %s is %.2f", name, mean_score)

    most = np.argmax(models_mean_scores)
    least = np.argmin(models_mean_scores)
    logging.info("The most accurate model is %s with mean score %.2f", models[most][0], models_mean_scores[most])
    logging.info("The least accurate model IS %s with mean score %.2f", models[least][0], models_mean_scores[least])

    logging.debug("%s", "\n".join([f"{name}: {models_mean_scores[i]}" for i, (name, model) in enumerate(models)]))

    return models[most][0], models_mean_scores[most]


if __name__ == "__main__":
    print(score_models())
