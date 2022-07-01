import pandas as pd
import numpy as np
import statsmodels.api as smt
from typing import Dict, Any, List
from challenger_v2 import signs_filter, existance_tester


class DataPreprocessing:
    def __init__(self):
        pass

    def output(self):
        pass

    def import_database(self):
        pass

    def select_stationarity(self):
        pass

    def clean_nonstationary(self):
        pass

    def correlation_filter(self):
        pass


class UniModel:
    def __init__(self, dep_dataset: list, ind_dataset: list, variables_dict: dict, sign_dict: dict):
        self.sign_dict = sign_dict
        self.ind_dataset = ind_dataset
        self.dep_dataset = dep_dataset
        self.variables_dict = variables_dict

    def model(self):
        pass

    def run(self):
        pass

    def export(self):
        pass


class BiModel:
    def __init__(self):
        self._bi_model = pd.DataFrame(
            {"Model Dependent": [], "Model Independent1": [], "Model Independent2": [], "Adj. R-Squared": [], "AIC": [],
             "F P-value": [],
             "Intercept": [], "Intercept pvalue": [], "Indep": [], "Indep pvalue": [], "Indep 2": [],
             "Indep 2 pvalue": [],
             "Sign Indep 1": [],
             "Sign Indep 2": []})

    def model(self):
        preprocessing = DataPreprocessing()

    def run(self, dep_dataset: list, ind_dataset: list, variables_dict: dict, sign_dict: dict):
        for dependent, ind in variables_dict.items():

            print("Current dependent {0}".format(dependent))
            cicle = 1

            for independent in ind:

                l = len(ind)
                # progress_bar(cicle, l)
                for independent_2 in ind:
                    if not existance_tester(independent_2, independent):
                        # print(independent_2)
                        y_train = dep_dataset[dependent]
                        x_train = ind_dataset[[independent, independent_2]]
                        x_train = smt.add_constant(x_train)
                        # x_train = np.asarray(x_train)

                        model = smt.OLS(y_train, x_train).fit()
                        print("Curent dependent variable: {} with current independent [{}, {}]".format(dependent,
                                                                                                       independent,
                                                                                                       independent_2))
                        sign1 = signs_filter(sign_dict, model.params.tolist()[1], independent)
                        sign2 = signs_filter(sign_dict, model.params.tolist()[2], independent_2)

                        result_df = {"Model Dependent": dependent, "Model Independent1": independent,
                                     "Model Independent2": independent_2,
                                     "Adj. R-Squared": model.rsquared_adj, "AIC": model.aic,
                                     "F P-value": model.f_pvalue, "Intercept": model.params.tolist()[0],
                                     "Intercept pvalue": model.pvalues.tolist()[0],
                                     "Indep": model.params.tolist()[1],
                                     "Indep pvalue": model.pvalues.tolist()[1],
                                     "Indep 2": model.params.tolist()[2],
                                     "Indep 2 pvalue": model.pvalues.tolist()[2], "Sign Indep 1": sign1,
                                     "Sign Indep 2": sign2}

                        pd.concat([self._bi_model, result_df], axis=0, ignore_index=True, sort=False)
                cicle += 1

    @staticmethod
    def export(data_to_export):
        return data_to_export
