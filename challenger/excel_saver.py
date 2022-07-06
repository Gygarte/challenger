import pandas as pd
import os
from pathlib import Path


def save_to_excel(data_to_save: list, path_to_save: Path, name_of_file: str) -> int:
    path_to_file = os.path.join(path_to_save, name_of_file)

    with pd.ExcelWriter(path_to_file) as saver:
        for index, files in enumerate(data_to_save):
            files.to_excel(saver, sheet_name=str(index))
    return 200
