import pandas as pd
from typing import Union

def import_databases(PATH: str, DOC: str, PORTFOLIO: str, DATABASE: pd.DataFrame) -> Union([pd.DataFrame, list]):

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

    port = pd.read_excel(PATH + DOC, sheet_name = PORTFOLIO)
    portfolio_data = pd.read_excel(PATH + DATABASE, sheet_name= "input")
    macro_data = pd.read_excel(PATH + DATABASE, sheet_name="macro")
    macro_col = macro_data.columns.values.tolist()

    return port, portfolio_data, macro_data, macro_col