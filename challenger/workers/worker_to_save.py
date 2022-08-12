import traceback
import sys
from pathlib import Path
from PyQt5.QtCore import QRunnable
from challenger.workers import worker_to_signal


class SaverWorker(QRunnable):
    def __init__(self,
                 saver_handler,
                 data_to_save: list,
                 path_to_save: Path,
                 name_of_file: str,
                 *args, **kwargs):

        super(SaverWorker, self).__init__()
        self.saver_handler = saver_handler
        self.data_to_save = data_to_save
        self.path_to_save = path_to_save
        self.name_of_file = name_of_file
        self.args = args
        self.kwargs = kwargs
        self.signals = worker_to_signal.SaveWorkerSignals()

        self.kwargs["done"] = self.signals.finished

    def run(self):
        try:
            self.saver_handler(self.data_to_save,
                               self.path_to_save,
                               self.name_of_file,
                               self.signals.finished)
            self.signals.finished.emit("Done")
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))