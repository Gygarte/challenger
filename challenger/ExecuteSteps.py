import pandas as pd
from PyQt5 import QtCore
from challenger.import_handler import ImportHandler
from challenger.ComputeModels import ComputeModels
from pathlib import Path


def select_stationary_dep(port):
    """
    @@@ Selects the stationary variables from the database @@@

    @@  Native only for versions that request user to pre-determine stationarity @@@

    @INPUT:
        port     - Required : database containing statioanry variables                  (pandas.DataFrame)
    @OUTPUT:
        dep_var             : list with the names of stationary dependent variables     (list)
        drop_var            : list with the names of non-stationary dependent variables (list)

    """
    dep_var = []
    drop_var = []
    for row_index in range(len(port)):
        if port.iat[row_index, 4] == "Seria este stationara":
            dep_var.append(port.iat[row_index, 0])
        else:
            drop_var.append(port.iat[row_index, 0])
    return dep_var, drop_var


class ExecuteSteps(QtCore.QObject):
    currentModel = QtCore.pyqtSignal(int)
    currentState = QtCore.pyqtSignal(str)
    _log = None
    _import_handler = ImportHandler()
    _model_algo = ComputeModels()

    def main(self, path_to_input: Path, stationary_doc: str, portfolio_name: str, input_database: str, sign_dict: dict,
             number_of_variables: int, stop_filter: bool):
        """
        It imports the data, cleans it, and then builds a univariate and bivariate model.
        """

        port, portfolio_data, macro_data, macro_col = self._import_handler.import_from_excel(path_to_input,
                                                                                             stationary_doc,
                                                                                             portfolio_name,
                                                                                             input_database)

        dependent_var, drop_var = select_stationary_dep(port)

        output_template = self._model_algo.build_template(number_of_variables)
        independent_var_combinations = self._model_algo.create_variable_combinations(macro_col, number_of_variables,
                                                                                     sign_dict)
        total_number_of_models = len(dependent_var) * len(independent_var_combinations)
        index = 1
        for dependent in dependent_var:
            self._log.info(f"Current dependent variable is {dependent}")
            for independent in independent_var_combinations:
                self._log.info(f"Current independent variable are {independent}")

                model_output = self._model_algo.compute_models(dependent, independent, data=portfolio_data)

                self._log.info(model_output)

                output = self._model_algo.save_output(model_output, output_template, sign_dict)

                self._log.info(f"Progress {index}/{total_number_of_models}")
                self._log.info(f"Current progress is {index}/{total_number_of_models}")

                self.currentModel.emit((index / total_number_of_models) * 100)

                index += 1
        # saving just for testing purposes
        output.to_excel(r"C:\Users\gabri\OneDrive\Desktop\Library\Challenger_script_v2\test\test.xlsx")
        return output

    def execute_challenger(self, path_to_input_file: Path,
                           input_file_name: str,
                           portfolio_sheet_name: str,
                           macro_sheet_name: str,
                           data_sheet_name: str,
                           number_of_variables: list,
                           sign_dict: dict) -> pd.DataFrame:

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

            self._log.info(f"Current computed number of varaibles is {number_of_var}")

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
                self.currentState.emit(dependent_var)
                for independent_var in independent_var_combinations:
                    self._log.info(f"Current independent variables are {independent_var}")

                    model_output = self._model_algo.compute_models(dependent_var, independent_var, data)

                    self._log.info(f"Current progress is {progress} / {total_number_of_models}")

                    output_from_model = self._model_algo.save_output(model_output, output_template, sign_dict)

                    self._log.info(f"Mode no.{progress} saved to output template!")

                    # Step#5.1: emit a signal to update the progress bar

                    self.currentModel.emit((progress / total_number_of_models) * 100)

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
