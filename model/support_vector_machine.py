import logging
import tempfile

from common import filename_for_archiving, load_csv_to_dataframe, measure_time, split_dataset
from constants import CACHE_SIZE_MB, PART_OF_DATA
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from skops.io import dump


def svm_model() -> Pipeline:
    return make_pipeline(
        StandardScaler(),
        SVC(
            kernel="linear",
            C=1.0,
            gamma="scale",
            class_weight="balanced",
            cache_size=CACHE_SIZE_MB,
            max_iter=250_000,
            verbose=True,
        ),
        verbose=True,
    )


@measure_time
def train_svm_model() -> float:
    pandas_dataframe = load_csv_to_dataframe(PART_OF_DATA)
    x_train, x_test, y_train, y_test = split_dataset(pandas_dataframe)
    logging.debug("Split dataset to training and test sets")

    with tempfile.TemporaryDirectory() as tmp_cache_dir:
        svc = svm_model()
        svc.memory = tmp_cache_dir

        logging.debug("Beginning training")
        svc.fit(x_train.values, y_train.values)
        logging.debug("Finished training")
        logging.debug("Number of iterations run %d", svc.named_steps.svc.n_iter_)
        logging.debug("Gamma used: %f", svc.named_steps.svc._gamma)  # pylint: disable=W0212

        test_acc = svc.score(x_test.values, y_test.values)
        print_acc = f"testing accuracy: {(test_acc * 100):.2f}"
        logging.info(print_acc)

        logging.debug("Saving model to disk")
        dump(svc, filename_for_archiving(f"ids_svm_model_{test_acc:.2f}"))

        return test_acc


if __name__ == "__main__":
    print(train_svm_model())
