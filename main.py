from challenger_v2 import *
from import_handler import *
from pathlib import Path


def main(path_to_input: Path, stationary_doc: str, portfolio_name: str, input_database: str, sign_dict: dict,
         treshold: float, stop_filter: bool) -> tuple:
    """
    It imports the data, cleans it, and then builds a univariate and bivariate model.
    """

    port, portfolio_data, macro_data, macro_col = import_databases(path_to_input, stationary_doc, portfolio_name,
                                                                   input_database)

    dependent_var, drop_var = select_stationary_dep(port)
    # frame(list(port.keys()))
    response = clean_nonstationary(drop_var, portfolio_data)  # de scos

    try:
        variables_dict = correlation_filter(dependent_var, macro_col, portfolio_data, macro_data, treshold, stop_filter)
        uni_model = uni_model_builder(response, macro_data, variables_dict, sign_dict)
        bi_model = bi_model_builder(response, macro_data, variables_dict, sign_dict)
    except Exception:
        variables_dict = correlation_filter(dependent_var, macro_col, portfolio_data, macro_data, treshold, stop_filter)
        uni_model = uni_model_builder(response, macro_data, variables_dict, sign_dict)
        bi_model = bi_model_builder(response, macro_data, variables_dict, sign_dict)

    print("Done processing model! Please save!")

    return (uni_model, bi_model)
