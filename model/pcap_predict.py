import logging
import os

from cicflowpy.convert_pcp_to_flow_csv import convert_pcap
from model_predict import load_input_csv_and_predict


def load_pcap_and_predict(pcap_filename: str, model_path: str | None = None) -> str:
    csv_filename = pcap_filename.replace(".pcap", ".csv")

    if os.path.exists(csv_filename):
        logging.debug("Skipping pcap conversion to csv since previous converted file %s exists", csv_filename)
        return load_input_csv_and_predict(csv_to_predict=csv_filename, model_to_use=model_path)

    return load_input_csv_and_predict(csv_to_predict=convert_pcap(pcap_filename), model_to_use=model_path)


if __name__ == "__main__":
    print(load_pcap_and_predict("in.pcap"))
