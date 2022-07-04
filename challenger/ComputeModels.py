import pandas as pd
import statsmodels.api as smt
from itertools import combinations


class ComputeModels:

    @staticmethod
    def compute_models(dependent_var: str, independent_var: tuple, data: pd.DataFrame,
                       intercept: int = 1):
        y_train = data[dependent_var]
        x_train = data[list(independent_var)]

        if intercept == 1:
            x_train = smt.add_constant(x_train)

        model = smt.OLS(y_train, x_train)
        model = model.fit()

        return [model, dependent_var, independent_var]

    @staticmethod
    def create_variable_combinations(list_of_var: list, number_of_var_for_combination: int,
                                     sign_dictionary: dict) -> list:
        assert number_of_var_for_combination <= len(list_of_var), Exception(
            "Cant compute combination larger than the input!")
        result = []
        # specific case for n = 1
        if number_of_var_for_combination == 1:
            for item in combinations(list_of_var, 1):
                result.append(item)
            return result

        # general case for n>=2 and n <= max len of variable list
        for item in combinations(list_of_var, number_of_var_for_combination):
            # print("Item is: {}".format(item))
            for index, key in enumerate(sign_dictionary.keys()):
                # print("Index is: {}".format(index))
                # print("Key is: {}".format(key))
                counter = 0
                for value in item:
                    if key in value:
                        counter += 1
                # print("Counter for item: {} is {}".format(item, counter))
                if counter > 1:
                    break
                elif index + 1 == len(sign_dictionary.keys()):
                    # print("Added item is {}".format(item))
                    result.append(item)
        return result

    def save_output(self, model_output, output_template: pd.DataFrame, sign_dict: dict) -> pd.DataFrame:
        model, dependent_var, independent_var = model_output[0], model_output[1], model_output[2]

        sign = self._sign_filter(sign_dict, model.params.tolist(), independent_var)
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
            # to solve the case when you dont put the coret sign dictionary
            # if the curent independnet does not have a corespondence in sign_dict
            # the sign dict does not produce an output for sign that are not in the dictionary
            try:
                add.append(sign[index])
            except IndexError:
                add.append("No sign available!")

        output_template.loc[len(output_template)] = add
        return output_template

    @staticmethod
    def _sign_filter(sign_dict: dict, model_coef: list, indep_var_combination: tuple) -> list:
        def _encode_coef_sign(coef: float) -> int:
            return -1 if coef < 0 else 1

        result = []
        for var, sign in sign_dict.items():
            for index, variable in enumerate(indep_var_combination):
                if var in variable:
                    if _encode_coef_sign(model_coef[index + 1]) == sign:
                        result.append("Correct!")
                    else:
                        result.append("Incorrect!")
        return result

    @staticmethod
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

    @staticmethod
    def _encode_coef_sign(coef: float) -> int:
        return -1 if coef < 0 else 1
