from typing import Dict, Any, List
import numpy as np
import pandas as pd
import statsmodels.api as smt
from signs_filter import signs_filter

"""IMPROVEMENT TO DO: make selecting the files path and portfolios through a GUI """


# function to select only the stationary dependent variables from the file provided
def select_stationary_dep(port):
    """
    @@@ Selects the stationary variables from the database @@@

    @@  Native only for versions that request user to pre-determine stationarity @@@
    
    @INPUT:
        port     - Required : database containing statioanry variables                  (pandas.DataFrame)
    @OUTPUT:
        dep_var             : list with the names of stationary dependent variables     (list)
        drop_var            : list with the names of non-stationary dependent variables (list)

    """
    dep_var = []
    drop_var = []
    for row_index in range(len(port)):
        if port.iat[row_index, 4] == "Seria este stationara":
            dep_var.append(port.iat[row_index, 0])
        else:
            drop_var.append(port.iat[row_index, 0])
    return dep_var, drop_var


# clearing the portfolio data from non-stationary variables
def clean_nonstationary(drop_col, data):
    """
    If the column exists, drop it. If it doesn't exist, return the dataframe.
    
    :param drop_col: a list of columns to drop
    :param data: the dataframe you want to clean
    :return: The dataframe with the column dropped.
    """
    try:
        data.drop(drop_col, axis=1)
        return data
    except:
        return data


def existance_tester(ind, ind_2):
    """
    It takes two strings, and returns True if the first string contains the first word of the second
    string
    
    :param ind: the index of the dataframe
    :param ind_2: the string that you want to check if it's in ind
    :return: A boolean value.
    """
    return (ind_2.split("_")[0] in ind.split("_")[0])


def duplicity_filter(cor_list):
    cor = {}
    for key, value in cor_list.items():
        final = list(dict.fromkeys(value))

        cor.update({key: final})
    return cor


# correlation filter
def correlation_filter(dependent_var: list, independent_var: list, dep_dataset: list, ind_dataset: list,
                       treshold: float, stop_filter: bool = False) -> Dict[Any, List[Any]]:
    """
    @@@ Filter the lists of dependent and independent variables using correlation between @@@

    @INPUT:
        dependent_var   - Required : list with dependent variables used for correlation                     (list)
        independent_var - Required : list with independent variables                                        (list)
        dep_dataset     - Required : dataset with the dependent variables series                            (pandas.DataFrame)
        ind_dataset     - Required : dataset with te independent variables series                           (pandas.DataFrame)
        treshold        - Required : value of the correlation at which variables are considered correlated  (float)
        stop_filter     - Required : boolean value for stopping the filter                                  (bool)

    @OUTPUT:
        cor_list                   : dictionary with key: dependnet variables and value: list with 
                                     the independent variabeles correlated                                  (dict)

    """

    cor_list = {}
    spam = []
    # appending the list of correlated variables above the treshold to the dictionary
    # the key is the dependent variables with which the independent is correlated
    if stop_filter:
        for dependent in dependent_var:
            for independent in independent_var:
                spam.append(independent)
            cor_list.update({dependent: spam})

        return duplicity_filter(cor_list)

    for dependent in dependent_var:
        for independent in independent_var:

            corelation = np.corrcoef(dep_dataset[dependent], ind_dataset[independent])[0][1]
            corelation = round(corelation, 4)

            if abs(corelation) >= treshold:
                spam.append(independent)

        cor_list.update({dependent: spam})

        # filtering for double values

    return duplicity_filter(cor_list)


def uni_model_builder(dep_dataset: list, ind_dataset: list, variables_dict: dict, sign_dict: dict) -> pd.DataFrame:
    """
    It takes a dependent and independent dataset, and a dictionary of variables, and returns a dataframe
    with the results of the univariate regression analysis
    
    :param sign_dict:
    :param dep_dataset: the dataframe containing the dependent variables
    :param ind_dataset: the independent variables dataset
    :param variables_dict: a dictionary of the variables you want to test. The key is the dependent
    variable, and the values are the independent variables
    :return: A dataframe with the results of the univariate model.
    """
    print("Uni Model builder Initialized...")

    uni_model = pd.DataFrame(
        {"Model Dependent": [], "Model Independent": [], "Adj. R-Squared": [], "AIC": [], "F P-value": [],
         "Intercept": [], "Intercept pvalue": [], "Indep": [], "Indep pvalue": [], "Sign": []})

    for dependent, values in variables_dict.items():

        print("Current dependent {0}".format(dependent))
        cicle = 1
        for independent in values:

            y_train = dep_dataset[dependent]
            x_train = ind_dataset[independent]
            x_train = smt.add_constant(x_train)
            # x_train = np.asarray(x_train)

            model = smt.OLS(y_train, x_train).fit()
            sign = signs_filter(sign_dict, model.params.tolist()[1], independent)
            print("Curent dependent variable: {} with current independent [{}]".format(dependent,
                                                                                      independent))
            uni_model = uni_model.append(
                {"Model Dependent": dependent, "Model Independent": independent, "Adj. R-Squared": model.rsquared_adj,
                 "AIC": model.aic,
                 "F P-value": model.f_pvalue, "Intercept": model.params.tolist()[0],
                 "Intercept pvalue": model.pvalues.tolist()[0],
                 "Indep": model.params.tolist()[1], "Indep pvalue": model.pvalues.tolist()[1], "Sign": sign},
                ignore_index=True)
            cicle += 1
    return uni_model


def bi_model_builder(dep_dataset: list, ind_dataset: list, variables_dict: dict, sign_dict: dict) -> pd.DataFrame:
    """
    It takes a dependent variable, an independent variable and a dictionary of variables as input and
    returns a dataframe with the results of the regression
    
    :param dep_dataset: the dataframe with the dependent variables
    :param ind_dataset: the independent variables
    :param variables_dict: a dictionary of the variables you want to test. The key is the dependent
    variable, and the value is a list of independent variables
    :return: A dataframe with the results of the bi-variate model.
    """

    print("Bi Model builder Initialized...")

    bi_model = pd.DataFrame(
        {"Model Dependent": [], "Model Independent1": [], "Model Independent2": [], "Adj. R-Squared": [], "AIC": [],
         "F P-value": [],
         "Intercept": [], "Intercept pvalue": [], "Indep": [], "Indep pvalue": [], "Indep 2": [], "Indep 2 pvalue": [],
         "Sign Indep 1": [],
         "Sign Indep 2": []})

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

                    bi_model = bi_model.append({"Model Dependent": dependent, "Model Independent1": independent,
                                                "Model Independent2": independent_2,
                                                "Adj. R-Squared": model.rsquared_adj, "AIC": model.aic,
                                                "F P-value": model.f_pvalue, "Intercept": model.params.tolist()[0],
                                                "Intercept pvalue": model.pvalues.tolist()[0],
                                                "Indep": model.params.tolist()[1],
                                                "Indep pvalue": model.pvalues.tolist()[1],
                                                "Indep 2": model.params.tolist()[2],
                                                "Indep 2 pvalue": model.pvalues.tolist()[2], "Sign Indep 1": sign1,
                                                "Sign Indep 2": sign2}, ignore_index=True)
            cicle += 1
    return bi_model
