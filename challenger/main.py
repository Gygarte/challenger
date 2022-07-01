from challenger.challenger_v2 import *
from challenger.import_handler import *
from compute_models import *
from challenger.compute_variable_combinations import create_variable_combinations
from pathlib import Path
from logging import log, INFO, basicConfig

basicConfig(level=INFO, filename="../out.log", filemode="w")

def main(path_to_input: Path, stationary_doc: str, portfolio_name: str, input_database: str, sign_dict: dict,
         number_of_variables: float, stop_filter: bool) -> tuple:
    """
    It imports the data, cleans it, and then builds a univariate and bivariate model.
    """

    port, portfolio_data, macro_data, macro_col = import_databases_from_excel(path_to_input, stationary_doc,
                                                                              portfolio_name,input_database)

    dependent_var, drop_var = select_stationary_dep(port)

    output_template = build_template(number_of_variables)
    independent_var_combinations = create_variable_combinations(macro_col, number_of_variables, sign_dict)
    total_number_of_models = len(dependent_var) * len(independent_var_combinations)
    index = 1
    for dependent in dependent_var:
        print(f"Current dependent variable is {dependent}")
        for independent in independent_var_combinations:
            print(f"Current independent variable are {independent}")
            model_output = compute_models(dependent, independent, data= portfolio_data)
            print(model_output)
            output = save_output(model_output, output_template, sign_dict)
            print(f"Progress {index}/{total_number_of_models}")
            print(f"Current progress is {index}/{total_number_of_models}")

            if index % 1000 == 0:
                print(output)
            index += 1
    output.to_excel(r"C:\Users\gabri\OneDrive\Desktop\Library\Challenger_script_v2\test\test.xlsx")
    return output
