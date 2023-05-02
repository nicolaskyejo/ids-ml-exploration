import logging
import tempfile

from common import dataset_to_x_and_y, filename_for_archiving, load_csv_to_dataframe, measure_time
from constants import ALL_DATA
from k_nearest_neighbor import knn_model
from logistic_regression import lr_model
from mlp_neural_network import mlp_model
from random_forest import random_forest_model
from skops.io import dump


@measure_time
def train_on_whole_dataset():
    model_pipelines = [
        knn_model(),
        # svm_model(), # not using since training time is quite high due to its time complexity
        random_forest_model(),
        mlp_model(),
        lr_model(),
    ]

    pandas_dataframe = load_csv_to_dataframe(ALL_DATA, nrows=None)
    features, targets = dataset_to_x_and_y(pandas_dataframe)
    logging.debug("Dataset loaded")

    for model_pipeline in model_pipelines:
        classifier_name = list(model_pipeline.named_steps.values())[-1].__class__.__name__

        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            classifier = model_pipeline
            classifier.memory = tmp_cache_dir

            logging.debug("Beginning training on full dataset: %s", classifier_name)
            classifier.fit(features.values, targets.values)
            logging.debug("Finished training on full dataset: %s", classifier_name)

            logging.debug("Saving model to disk")
            dump(classifier, filename_for_archiving(f"production_{classifier_name.lower()}_model"))


if __name__ == "__main__":
    train_on_whole_dataset()
