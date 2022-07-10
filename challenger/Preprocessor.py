from PyQt5.QtCore import QObject
from PyQt5 import QtCore
from typing import Union, Any, Tuple, List
from pathlib import Path
from pandas import DataFrame
from challenger.import_handler import ImportHandler
from challenger.ComputeModels import ComputeModels


class Preprocessor(QObject):

    def __init__(self,
                 path_to_input_file: Union[Path, str],
                 input_file_name: str,
                 portfolio_sheet_name: str,
                 macro_sheet_name: str,
                 data_sheet_name: str,
                 number_of_variables: int,
                 sign_dict: dict
                 ):

        self.sign_dict = sign_dict
        self.number_of_variables = number_of_variables
        self.data_sheet_name = data_sheet_name
        self.macro_sheet_name = macro_sheet_name
        self.portfolio_sheet_name = portfolio_sheet_name
        self.input_file_name = input_file_name
        self.path_to_input_file = path_to_input_file

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

    def run_preprocess(self) -> Tuple[List[Tuple[Any, Any]], DataFrame, DataFrame]:

        self._log.info(f"Current computed number of variables is {self.number_of_variables}")

        output_template = self._models.build_template(self.number_of_variables)

        # run import method for retrieving the necessary data

        portfolio_dependent, macro_var, data = self._import_data()

        independent_var_combinations = self._models.create_variable_combinations(macro_var,
                                                                                 self.number_of_variables,
                                                                                 self.sign_dict)
        data_for_executor = []

        self._total_number_of_models = len(portfolio_dependent) * len(independent_var_combinations)
        for dependent in portfolio_dependent:
            for independent in independent_var_combinations:
                data_for_executor.append((dependent, independent))

        return data_for_executor, output_template, data

    @property
    def log(self):
        return self._log

    @log.setter
    def set_log(self, logger):
        self._log = logger

    @property
    def total_number_of_models(self):
        return self._total_number_of_models
