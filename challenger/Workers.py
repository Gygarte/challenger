import traceback
import sys
from PyQt5.QtCore import QRunnable, QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from challenger.ExecuteSteps import ExecuteSteps
from pathlib import Path


class WorkerSignals(QObject):
    """
    Used signals:

    finished: No data
    error: tuple (exctype, value, traceback.format_exc())
    result: object data => Pandas DataFrame
    progress: int - returned from main processing class


    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


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
        self.signals = WorkerSignals()

        self.kwargs["done"] = self.signals.finished

    def run(self):
        try:
            self.saver_handler(self.data_to_save,
                               self.path_to_save,
                               self.name_of_file,
                               self.signals.finished)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))


class ProcessingWorker(QRunnable):
    def __init__(self, executer_class: ExecuteSteps,
                 path_to_input_file: str,
                 input_file_name: str,
                 portfolio_sheet_name: str,
                 macro_sheet_name: str,
                 data_sheet_name: str,
                 number_of_variables: list,
                 sign_dict: dict, *args, **kwargs):
        super(ProcessingWorker, self).__init__()
        self.exe = executer_class
        self.path_to_input_file = path_to_input_file
        self.input_file_name = input_file_name
        self.portfolio_sheet_name = portfolio_sheet_name
        self.macro_sheet_name = macro_sheet_name
        self.data_sheet_name = data_sheet_name
        self.number_of_variables = number_of_variables
        self.sign_dict = sign_dict
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.exe.execute_challenger(
                self.path_to_input_file,
                self.input_file_name,
                self.portfolio_sheet_name,
                self.macro_sheet_name,
                self.data_sheet_name,
                self.number_of_variables,
                self.sign_dict,
                self.signals.progress
            )

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
