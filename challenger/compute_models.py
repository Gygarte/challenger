import pandas as pd
# from challenger.signs_filter import signs_filter
import statsmodels.api as smt


def encode_coef_sign(coef: float):
    return -1 if coef < 0 else 1


def sign_filter(sign_dict: dict, model_coef: list, indep_var_combination: tuple) -> list:
    result = []
    for var, sign in sign_dict.items():
        for index, variable in enumerate(indep_var_combination):
            if var in variable:
                if encode_coef_sign(model_coef[index + 1]) == sign:
                    result.append("Correct!")
                else:
                    result.append("Incorrect!")
    return result


def compute_models(dependent_var: str, independent_var: tuple, data: pd.DataFrame,
                   intercept: int = 1):
    y_train = data[dependent_var]
    x_train = data[list(independent_var)]

    if intercept == 1:
        x_train = smt.add_constant(x_train)

    model = smt.OLS(y_train, x_train)
    model = model.fit()

    return [model, dependent_var, independent_var]


def build_template(n_independent):
    output = pd.DataFrame({"Dependent": []})
    # adding the number of columns for each independent variable
    for index in range(1, n_independent + 1):
        add = pd.DataFrame({f"Independent_{index}": []})
        output = pd.concat([output, add])

    # adding the number of columns for model quality parameters
    model_quality = pd.DataFrame(
        {"Adj.R-Squared": [], "AIC": [], "F Pvalue": [], "Intercept": [], "Intercept pvalue": []})
    output = pd.concat([output, model_quality])

    for index in range(1, n_independent + 1):
        add = pd.DataFrame({f"Coef_{index}": [], f"Pvalue_{index}": [], f"Sign_{index}": []})
        output = pd.concat([output, add])
    return output


def save_output(model_output, output_template: pd.DataFrame, sign_dict: dict) -> pd.DataFrame:
    model, dependent_var, independent_var = model_output[0], model_output[1], model_output[2]

    sign = sign_filter(sign_dict, model.params.tolist(), independent_var)
    model_coef = model.params.tolist()
    model_pvalues = model.pvalues.tolist()

    add = [dependent_var]
    for name in independent_var:
        add.append(name)

    add.append(model.rsquared_adj)
    add.append(model.aic)
    add.append(model.f_pvalue)
    add.append(model_coef[0])
    add.append(model_pvalues[0])

    for index, value in enumerate(independent_var):
        add.append(model_coef[index + 1])
        add.append(model_pvalues[index + 1])
        #to solve the case when you dont put the coret sign dictionary
        #if the curent independnet does not have a corespondence in sign_dict
        #the sign dict does not produce an output for sign that are not in the dictionary
        try:
            add.append(sign[index])
        except IndexError:
            add.append("No sign available!")

    output_template.loc[len(output_template)] = add
    return output_template


__all__ = ["save_output", "build_template", "compute_models"]

