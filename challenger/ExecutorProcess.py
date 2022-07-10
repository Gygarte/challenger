from multiprocessing import Process, Queue
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from pandas import DataFrame

from challenger.ComputeModels import ComputeModels
from challenger.import_handler import ImportHandler
from pathlib import Path
from typing import Union, List, Tuple, Any


class ProcessStatus(QObject):
    status = QtCore.pyqtSignal()


class ExecutorProcess(Process):
    def __init__(self, logger, instructions, data, *args, **kwargs):
        super(Process, self).__init__()
        self.__queue = Queue()
        self.__signal_status = ProcessStatus()
        self._logger = logger
        self._instructions = instructions
        self._data = data

    def run(self) -> None:
        # it should accept a tuple of form (independent variable, (dependent variable set))
        # the tuples are in a list => build a function that create all the combinations - iterable way to save memory
        # args = [logger, executor_data]
        executor = Executor()
        # set the logger in executor class
        executor.set_log = self.args[0]

        result = executor.execute(self.args[1])

        self.__queue.put((self.__signal_status.status, result))





class Executor(QObject):

    def __init__(self, logger, instructions: list, data: DataFrame, *args, **kwargs):
        self._logger = logger
        self._instructions = instructions
        self._data = data

    _model = ComputeModels()

    # data = [dependent, independent_set, calculation_data]
    def execute(self) -> Any:

        self._log.info(f"Current dependent variable is {self._instructions[0]}")
        self._log.info(f"Current independent variables are {self._instructions[1]}")

        return self._model.compute_models(self._instructions[0], self._instructions[1], self._data)

    @property
    def log(self):
        return self._log

    @log.setter
    def set_logger(self, logger):
        self._log = logger
