import multiprocessing as mp
import traceback
import sys
import time
from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import pyqtSlot
from challenger.old.ExecuteSteps import ExecuteSteps
from challenger.old.compute_models import compute_models_modified
from pandas import DataFrame

import dill


def helperFunction(function, inp, *args, **kwargs):
    # reimport, just in case this is not available on the new processes
    function = dill.loads(function)  # converts bytes to (potentially lambda) function
    return function(inp, *args, **kwargs)






class ExecutorWorker(QRunnable):
    """Implement the process that handles the execution of the algorithm"""

    def __init__(self, logger, instructions: list, data: DataFrame) -> None:
        super(QRunnable, self).__init__()
        self._logger = logger
        self._instructions = instructions
        self._data = data

        self.signals = ExecutorWorkerSignals()

        self.executor = compute_models_modified
        self.executor.set_logger = self._logger
        # set Process Pool
        self.pool = mp.Pool(4)

    def run(self):
        try:
            self.signals.start.emit()
            t0 = time.perf_counter()
            result = self.pool.map(self.executor, [(item, self._data) for item in self._instructions])
            t1 = time.perf_counter()
            self.signals.result.emit(t1-t0)


        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()


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
