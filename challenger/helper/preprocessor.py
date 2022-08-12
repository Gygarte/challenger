from PyQt5.QtCore import QObject
from PyQt5 import QtCore
from typing import Any, Tuple, List, Callable, Generator

from numpy import ndarray
from pandas import DataFrame
from challenger.helper.import_handler import ImportHandler
from challenger.old.compute_models import ComputeModels


class Preprocessor(QObject):

    def __init__(self, input_data: dict) -> None:

        self.sign_dict = input_data.get("sign_dict")
        self.number_of_variables = input_data.get("number_of_variables")[0]
        self.data_sheet_name = input_data.get("data_sheet_name")
        self.macro_sheet_name = input_data.get("macro_sheet_name")
        self.portfolio_sheet_name = input_data.get("portfolio_sheet_name")
        self.input_file_name = input_data.get("input_file_name")
        self.path_to_input_file = input_data.get("path_to_input_folder")
        print(self.path_to_input_file)

    _log = None

    _status = QtCore.pyqtSignal(tuple)
    _import_handler = ImportHandler()
    _models = ComputeModels()
    _total_number_of_models = None

    def _import_data(self) -> Tuple[Any, Any, DataFrame]:

        # handler the import segment of the whole process
        portfolio_dependent, macro_var, data = self._import_handler.import_from_excel2(self.path_to_input_file,
                                                                                       self.input_file_name,
                                                                                       self.portfolio_sheet_name,
                                                                                       self.macro_sheet_name,
                                                                                       self.data_sheet_name)

        self._log.info(f"Current portfolio is {self.portfolio_sheet_name} from address {self.path_to_input_file}")

        return portfolio_dependent, macro_var, data

    def run(self) -> tuple[Callable[[], Generator[tuple[Any, Any, tuple[Any, Any]], Any, None]], DataFrame]:

        self._log.info(f"Current computed number of variables is {self.number_of_variables}")

        output_template = self._models.build_template(self.number_of_variables)

        # run import method for retrieving the necessary data

        portfolio_dependent, macro_var, data = self._import_data()

        independent_var_combinations = self._models.create_variable_combinations(macro_var,
                                                                                 self.number_of_variables,
                                                                                 self.sign_dict)
        data_in = []

        self._total_number_of_models = len(portfolio_dependent) * len(independent_var_combinations)

        def generator():

            for dependent in portfolio_dependent:
                for independent in independent_var_combinations:
                    yield (data[dependent].to_numpy(), data[list(independent)].to_numpy(), (dependent, independent))

        return generator, output_template

    @property
    def log(self):
        return self._log

    @log.setter
    def set_log(self, logger):
        self._log = logger

    @property
    def total_number_of_models(self):
        return self._total_number_of_models
