import pandas as pd
import os
from pathlib import Path


def save_to_excel(data_to_save: tuple, path_to_save: Path, name_to_save: str) -> int:
    path_to_file = os.path.join(path_to_save, name_to_save)

    with pd.ExcelWriter(path_to_file) as saver:
        for files in data_to_save:
            files.to_excel(saver, sheet_name=str(files))
    return 200
