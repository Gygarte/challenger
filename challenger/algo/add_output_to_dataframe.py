import pandas as pd
from challenger.algo import sign_filter
from statsmodels.regression.linear_model import RegressionResults


def add_output_to_dataframe(self, model_output: RegressionResults, output_template: pd.DataFrame,
                            sign_dict: dict) -> pd.DataFrame:
    model, dependent_var, independent_var = model_output[0], model_output[1], model_output[2]

    sign = self._sign_filter(sign_dict, model.params.tolist(), independent_var)
    model_coef = model.params.tolist()
    model_pvalues = model.pvalues.tolist()

    output_as_dict: dict = {"Dependent": dependent_var}
    for index, name in enumerate(independent_var):
        output_as_dict.update({f"Independent_{index + 1}": name})

    output_as_dict.update({"Adj.R-Squared": model.rsquared_adj,
                           "AIC": model.aic,
                           "F Pvalue": model.f_pvalue,
                           "Intercept": model_coef[0],
                           "Intercept pvalue": model_pvalues[0]})

    for index, value in enumerate(independent_var):
        output_as_dict.update({f"Coef_{index + 1}": model_coef[index + 1]})
        output_as_dict.update({f"Pvalue_{index + 1}": model_pvalues[index + 1]})

        # to solve the case when you dont put the coret sign dictionary
        # if the curent independnet does not have a corespondence in sign_dict
        # the sign dict does not produce an output for sign that are not in the dictionary
        try:
            output_as_dict.update({f"Sign_{index + 1}": sign[index]})

        except IndexError:
            output_as_dict.update({f"Sign_{index + 1}": "No sign available!"})

    output_template.loc[len(output_template)] = output_as_dict

    return output_template


def output_to_dataframe(output_of_processing: list[dict], sign_dict: dict, type_of_model: int) -> pd.DataFrame:
    for item in output_of_processing:
        model_coef: list[float] = [item.get(f"Independent_{index + 1}_coef") for index in range(type_of_model)]
        model_independent: list[str] = [item.get(f"Independent_{index + 1}") for index in range(type_of_model)]
        sign: list[str] = sign_filter.sign_filter(sign_dict, model_coef, model_independent)

        # update the outputs with sign
        try:
            for index in range(type_of_model):
                item.update({f"Independent_{index + 1}_sign": sign[index]})
        except IndexError:
            item.update({f"Sign Error": "No Sign"})

    return pd.DataFrame(output_of_processing)
