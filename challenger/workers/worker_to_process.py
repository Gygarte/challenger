import traceback
import sys
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import pyqtSlot
from challenger.workers import worker_to_signal
from challenger.old import ExecuteSteps

"""
Old Worker that uses the old processor class
"""


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
        self.signals = worker_to_signal.WorkerSignals()

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
