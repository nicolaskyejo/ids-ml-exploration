import glob
import os
from collections import Counter
from datetime import date

from pcap_predict import load_pcap_and_predict

PCAP_PATH = "./benign/"
MODEL_PATH = "./trained_models/"


def predict_all():
    model_pattern = "*.skops"
    pcap_pattern = "*.pcap"

    pcap_files = sorted(glob.glob(PCAP_PATH + pcap_pattern), key=os.path.getsize)
    model_files = sorted(glob.glob(MODEL_PATH + model_pattern), key=os.path.getsize)

    false_positives = Counter()  # predicted malicious while it is benign aka 'noise'
    false_negatives = Counter()  # predicted benign while it is malicious aka 'missed'
    true_predictions = Counter()  # predicted correctly

    with open(f"{date.today()}_predictions_for_benign_traffic.txt", "w+", encoding="utf-8") as file_descriptor:
        for pcap_file_path in pcap_files:
            pcap_file = os.path.basename(pcap_file_path)
            file_descriptor.write(f"For pcap file 📄 {pcap_file}\n")

            for model_file_path in model_files:
                prediction = load_pcap_and_predict(pcap_filename=pcap_file_path, model_path=model_file_path)
                model_file = os.path.basename(model_file_path)

                file_descriptor.write(f"Model {model_file} predicted ➡➡➡ {prediction}\n")

                is_benign = "benign" in pcap_file.lower()
                match prediction, is_benign:
                    case "BENIGN", True:
                        true_predictions.update({model_file: 1})
                    case "BENIGN", False:
                        false_negatives.update({model_file: 1})
                    case "MALICIOUS", True:
                        false_positives.update({model_file: 1})
                    case "MALICIOUS", False:
                        true_predictions.update({model_file: 1})

            file_descriptor.write("#" * 79 + "\n")

        file_descriptor.write("\n")
        file_descriptor.write(f"True predictions ✅ -> {true_predictions}\n\n")
        file_descriptor.write(f"False positives ❎ -> {false_positives}\n\n")
        file_descriptor.write(f"False negatives ❌ -> {false_negatives}\n\n")

        if len(true_predictions) > 0:
            file_descriptor.write(
                f"Most true predictions model is {true_predictions.most_common(1)[0][0]} with prediction accuracy of"
                f" {(true_predictions.most_common(1)[0][1] / len(pcap_files) * 100):.2f}\n"
            )

        # todo won't write 0 predictions
        if len(true_predictions) > 1:
            file_descriptor.write(
                f"Least true predictions model is {true_predictions.most_common()[-1][0]} with prediction accuracy of"
                f" {(true_predictions.most_common()[-1][1] / len(pcap_files) * 100):.2f}\n"
            )


if __name__ == "__main__":
    predict_all()
