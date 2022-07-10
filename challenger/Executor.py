from PyQt5.QtCore import QObject
from pandas import DataFrame
from challenger.ComputeModels import ComputeModels
from typing import Any


class Executor(QObject):

    def __init__(self,  data: DataFrame, *args, **kwargs):
        super(QObject, self).__init__()
        self._logger = None
        self._data = data

    _model = ComputeModels()

    # data = [dependent, independent_set, calculation_data]
    def execute(self, instructions) -> Any:
        self._logger.info(f"Current dependent variable is {instructions[0]}")
        self._logger.info(f"Current independent variables are {instructions[1]}")

        return self._model.compute_models(instructions[0], instructions[1], self._data)

    @property
    def log(self):
        return self._logger

    @log.setter
    def set_logger(self, logger):
        self._logger = logger
