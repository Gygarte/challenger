import multiprocessing as mp
import traceback
import sys
import time
from PyQt5.QtCore import QRunnable, QObject
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from challenger.ExecuteSteps import ExecuteSteps
from challenger.Preprocessor import Preprocessor
from challenger.Executor import Executor
from challenger.ComputeModels import compute_models_modified
from pathlib import Path
from typing import Union
from pandas import DataFrame

import dill


def helperFunction(function, inp, *args, **kwargs):
    # reimport, just in case this is not available on the new processes
    function = dill.loads(function)  # converts bytes to (potentially lambda) function
    return function(inp, *args, **kwargs)


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


class PreprocessingWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class ExecutorWorkerSignals(QObject):
    start = pyqtSignal()
    finished = pyqtSignal()
    status = pyqtSignal(int)
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


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


class PreprocessingWorker(QRunnable):
    """
    Implements the preprocessing stage in a different thread
    """

    def __init__(self,
                 path_to_input_file: Union[Path, str],
                 input_file_name: str,
                 portfolio_sheet_name: str,
                 macro_sheet_name: str,
                 data_sheet_name: str,
                 number_of_variables: int,
                 sign_dict: dict):

        self.signals = PreprocessingWorkerSignals()
        self.preprocessor = Preprocessor(path_to_input_file,
                                         input_file_name,
                                         portfolio_sheet_name,
                                         macro_sheet_name,
                                         data_sheet_name,
                                         number_of_variables,
                                         sign_dict)

    def run(self):
        try:
            result = self.preprocessor.run_preprocess()
            total_number_of_models = self.preprocessor.total_number_of_models()
            self.signals.result.emit((result, total_number_of_models))
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()


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
        self.pool = mp.Pool(mp.cpu_count() - 4)

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
