import pandas as pd
import os
from pathlib import Path
from PyQt5.QtCore import pyqtSignal


def save_to_excel(data_to_save: pd.DataFrame, path_to_save: Path, name_of_file: str, *done: pyqtSignal) -> int:
    path_to_file = os.path.join(path_to_save, name_of_file)

    with pd.ExcelWriter(path_to_file) as saver:
        data_to_save.to_excel(saver, sheet_name="Output")
        print("Saved")