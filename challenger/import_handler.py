import pandas as pd
import os
from pathlib import Path
from typing import Any, Union


class ImportHandler:
    """
            @@@ Call in pandas functions to read the database (excell filetype) @@@

            @INPUT:
                PATH      - Required :  path to the working directory, containing and the database (str)
                DOC       - Required :  name of document containing the list of stationary dependent variables (str)
                PORTFOLIO - Required :  name of the portfolio coresponding to the containing sheet (str)
                DATABASE  - Required :  database containing the values for each variable (str)
                                     :  has two sheets - input for dependent variable and macro - for macro variables (str)

            @OUTPUT:
                port                 : stationary dependent variable (pandas.dataframe)
                portfolio_data       : dependent variables values (pandas.dataframe)
                macro_data           : macro data (pandas.dataframe)
                macro_col            : macro data columns names (list)

            """

    @staticmethod
    def import_from_excel(PATH: Path, DOC: str, PORTFOLIO: str, DATABASE: str) -> Any:
        port = pd.read_excel(os.path.join(PATH, DOC), sheet_name=PORTFOLIO)
        portfolio_data = pd.read_excel(os.path.join(PATH, DATABASE), sheet_name="input")
        macro_data = pd.read_excel(os.path.join(PATH, DATABASE), sheet_name="macro")
        macro_col = macro_data.columns.values.tolist()

        return port, portfolio_data, macro_data, macro_col

    @staticmethod
    def import_from_csv(PATH: Path, DOC: str, PORTFOLIO: str, DATABASE: str) -> Any:
        port = pd.read_csv(os.path.join(PATH, DOC), sheet_name=PORTFOLIO)
        portfolio_data = pd.read_csv(os.path.join(PATH, DATABASE), sheet_name="input")
        macro_data = pd.read_csv(os.path.join(PATH, DATABASE), sheet_name="macro")
        macro_col = macro_data.columns.values.tolist()

        return port, portfolio_data, macro_data, macro_col

    @staticmethod
    def import_from_excel2(path: Union[Path, str],
                           input_file_name: str,
                           portfolio_sheet_name: str,
                           macro_sheet_name: str = "macro",
                           data_sheet_name: str = "input") -> Any:
        portfolio_dependent = pd.read_excel(os.path.join(path, input_file_name), sheet_name=portfolio_sheet_name)
        macro_var = pd.read_excel(os.path.join(path, input_file_name), sheet_name=macro_sheet_name)
        data = pd.read_excel(os.path.join(path, input_file_name), sheet_name=data_sheet_name)

        # converting to lists
        portfolio_dependent = portfolio_dependent[portfolio_dependent.columns.tolist()[0]].tolist()
        macro_var = macro_var[macro_var.columns.tolist()[0]].tolist()

        return portfolio_dependent, macro_var, data

    @staticmethod
    def import_from_csv2(path: Union[Path, str],
                         input_file_name: str,
                         portfolio_sheet_name: str,
                         macro_sheet_name: str = "macro",
                         data_sheet_name: str = "input") -> Any:
        portfolio_dependent = pd.read_csv(os.path.join(path, input_file_name), sheet_name=portfolio_sheet_name)
        macro_var = pd.read_csv(os.path.join(path, input_file_name), sheet_name=macro_sheet_name)
        data = pd.read_csv(os.path.join(path, input_file_name), sheet_name=data_sheet_name)

        # converting to lists
        portfolio_dependent = portfolio_dependent[portfolio_dependent.columns.tolist()[0]].tolist()
        macro_var = macro_var[macro_var.columns.tolist()[0]].tolist()

        return portfolio_dependent, macro_var, data
