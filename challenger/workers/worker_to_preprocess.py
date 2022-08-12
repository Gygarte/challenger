import traceback
import sys
from pathlib import Path
from PyQt5.QtCore import QRunnable
from challenger.helper import preprocessor
from typing import Union
import worker_to_signal


class PreprocessingWorker(QRunnable):
    """
    Implements the preprocessing stage in a different thread
    """

    def __init__(self, data_in: dict) -> None:

        self.signals = worker_to_signal.PreprocessingWorkerSignals()
        self.preprocessor = preprocessor.Preprocessor(data_in)

    def run(self):
        try:
            result = self.preprocessor.run()
            total_number_of_models = self.preprocessor.total_number_of_models()
            self.signals.result.emit((result, total_number_of_models))
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
