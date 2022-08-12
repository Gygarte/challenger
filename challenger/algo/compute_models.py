import statsmodels.api as smt
import pandas as pd
from typing import List, Tuple, Union

from statsmodels.regression.linear_model import RegressionResults


def compute_models_modified(data_in: tuple, data: pd.DataFrame) -> list[Union[RegressionResults, str]]:
    dependent_var: str = data_in[0]
    independent_var: str = data_in[1]
    data = data

    y_train = data[dependent_var]
    x_train = data[list(independent_var)]

    x_train = smt.add_constant(x_train)

    model = smt.OLS(y_train, x_train)
    model = model.fit()

    return [model, dependent_var, independent_var]
