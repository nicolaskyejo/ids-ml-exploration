import logging
import tempfile

from common import filename_for_archiving, load_csv_to_dataframe, measure_time, split_dataset
from constants import PART_OF_DATA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from skops.io import dump


def lr_model() -> Pipeline:
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(solver="lbfgs", class_weight="balanced", verbose=1, max_iter=1_000),
        verbose=False,
    )


@measure_time
def train_logistic_regression_model() -> float:
    pandas_dataframe = load_csv_to_dataframe(PART_OF_DATA)
    x_train, x_test, y_train, y_test = split_dataset(pandas_dataframe)
    logging.debug("Split dataset to training and test sets")

    with tempfile.TemporaryDirectory() as tmp_cache_dir:
        logit = lr_model()
        logit.memory = tmp_cache_dir

        logging.debug("Beginning training")
        logit.fit(x_train.values, y_train.values)
        logging.debug("Finished training")

        test_acc = logit.score(x_test.values, y_test.values)
        print_acc = f"testing accuracy: {(test_acc * 100):.2f}"
        logging.info(print_acc)

        logging.debug("Saving model to disk")
        dump(logit, filename_for_archiving(f"ids_logit_model_{test_acc:.2f}"))

        return test_acc


if __name__ == "__main__":
    print(train_logistic_regression_model())
