import pandas as pd
from PyQt5 import QtCore
from challenger.helper.import_handler import ImportHandler
from challenger.old.compute_models import ComputeModels
from pathlib import Path

"""
Old executor _ to be deleted oance teh parallel processor is in place

NOTE: is working properly, but takes a lot of time to finish
"""

class ExecuteSteps(QtCore.QObject):
    _log = None
    _import_handler = ImportHandler()
    _model_algo = ComputeModels()

    def execute_challenger(self, path_to_input_file: Path,
                           input_file_name: str,
                           portfolio_sheet_name: str,
                           macro_sheet_name: str,
                           data_sheet_name: str,
                           number_of_variables: list,
                           sign_dict: dict,
                           progress_callback:QtCore.pyqtSignal) -> pd.DataFrame:

        # Step#1: import data from input file - this is a stupid comment

        portfolio_dependent, macro_var, data = self._import_handler.import_from_excel2(path_to_input_file,
                                                                                       input_file_name,
                                                                                       portfolio_sheet_name,
                                                                                       macro_sheet_name,
                                                                                       data_sheet_name
                                                                                       )
        self._log.info(f"Current porfolio is {portfolio_sheet_name} from address {path_to_input_file}")

        global_output = []
        output_from_model = None
        # Step#2: loop through number_of_variable to compute models with the specified number of independent variables
        for number_of_var in number_of_variables:

            self._log.info(f"Current computed number of variables is {number_of_var}")

            # Step#3: build an output template for the current number of variables
            output_template = self._model_algo.build_template(number_of_var)

            # Step#4: compute combinations of independent variables

            independent_var_combinations = self._model_algo.create_variable_combinations(macro_var,
                                                                                         number_of_var,
                                                                                         sign_dict)

            # process variables
            progress = 1
            total_number_of_models = len(portfolio_dependent) * len(independent_var_combinations)

            # Step#5: iter through each dependent variable and compute models with each independent variables set
            for dependent_var in portfolio_dependent:

                self._log.info(f"Current dependent variable is {dependent_var}")

                # emit a signal with the current state

                for independent_var in independent_var_combinations:
                    self._log.info(f"Current independent variables are {independent_var}")

                    model_output = self._model_algo.compute_models(dependent_var, independent_var, data)

                    self._log.info(f"Current progress is {progress} / {total_number_of_models}")

                    output_from_model = self._model_algo.save_output(model_output, output_template, sign_dict)

                    self._log.info(f"Mode no.{progress} saved to output template!")

                    # Step#5.1: emit a signal to update the progress bar

                    progress_callback.emit(int((progress / total_number_of_models) * 100))

                    progress += 1
            self._log.info("Global output appended!")
            print(output_from_model)
            # Step#6: append the output to global output list
            global_output.append(output_from_model)
        self._log.info("Ready for saving!")
        # Step#7: return global results
        return global_output

    @property
    def log(self):
        return self._log

    @log.setter
    def set_log(self, logger):
        self._log = logger
