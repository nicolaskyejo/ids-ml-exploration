import tkinter as tk
from tkinter import filedialog, messagebox

from pcap_predict import load_pcap_and_predict


class SimpleFileOpener:
    """A class for managing opening and prediction of pcap files with Tcl/Tk python interface"""

    def __init__(self, root):
        self.manager = root

        self.pcap_file_path = None
        self.model_file_path = None
        self.model_file_path_label = tk.Label(self.manager, text="")
        self.pcap_file_path_label = tk.Label(self.manager, text="")

        self.manager.title("Predict Captured Traffic")
        tk.Label(self.manager, text="Open the full packet capture you want to predict").pack(pady=80, padx=80)

        self.pcap_file_path_label.pack(pady=10)
        self.model_file_path_label.pack(pady=40)

        tk.Button(
            self.manager,
            text="Select Model File (*.skops)",
            foreground="gold",
            background="black",
            relief="raised",
            cursor="diamond_cross",
            justify="center",
            command=self.open_model,
        ).pack()

        tk.Button(
            self.manager,
            text="Select PCAP File",
            foreground="white",
            background="black",
            relief="raised",
            cursor="diamond_cross",
            justify="center",
            command=self.open_pcap,
        ).pack()

        tk.Button(
            self.manager,
            text="Predict",
            foreground="orange",
            background="black",
            relief="raised",
            cursor="diamond_cross",
            command=self.call_predict,
        ).pack()

    def open_pcap(self):
        file_path = filedialog.askopenfilename(filetypes=[("pcap Files", "*.pcap")])
        self.pcap_file_path = file_path if file_path != "" else self.pcap_file_path
        self.pcap_file_path_label.config(text=truncate_path(prefix="pcap: ", path=self.pcap_file_path))

    def open_model(self):
        file_path = filedialog.askopenfilename(filetypes=[("skops Models", "*.skops")])
        self.model_file_path = file_path if file_path != "" else self.model_file_path
        self.model_file_path_label.config(text=truncate_path(prefix="model: ", path=self.model_file_path))

    def call_predict(self):
        if self.pcap_file_path is None:
            messagebox.showerror(message="No file chosen!")
            return

        prediction = load_pcap_and_predict(pcap_filename=self.pcap_file_path, model_path=self.model_file_path)
        color = "red" if prediction == "MALICIOUS" else "green"

        dialog = tk.Toplevel()
        dialog.title("Prediction label for traffic")

        tk.Label(dialog, text=prediction, foreground=color).pack(padx=20, pady=20)

        button = tk.Button(dialog, text="OK", command=dialog.destroy)
        button.pack(padx=10, pady=10)
        button.focus_set()

        # Make the dialog modal to prevent interaction with the parent window
        dialog.transient(self.manager)
        dialog.grab_set()
        self.manager.wait_window(dialog)


def truncate_path(prefix: str, path: str, last_n_chars: int = 60) -> str:
    if len(path) <= last_n_chars:
        return prefix + path
    return prefix + "..." + path[-last_n_chars:]


def main():
    root = tk.Tk()
    root.geometry("640x480")
    SimpleFileOpener(root)
    root.mainloop()


if __name__ == "__main__":
    main()
