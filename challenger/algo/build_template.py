import pandas as pd


def build_template(n_independent: int) -> pd.DataFrame:
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
