import string
import pandas as pd

def signs_filter(sign_dict: dict, param: float, independent1: str, independent2: str = None) -> str:
    """
    It takes in a dictionary of signs, a parameter, and two independent variables. It then checks if the
    parameter is in the independent variables, and if it is, it checks if the sign of the parameter
    matches the sign of the independent variable. If it does, it returns "Correct", otherwise it returns
    "Incorrect"
    
    :param sign_dict: a dictionary of the signs and their corresponding values
    :param param: the parameter that you want to check the sign of
    :param independent1: The independent variable that you want to test
    :param independent2: The independent variable that you want to test
    :return: a string "Correct" if the sign of the parameter is the same as the sign of the independent
    variable. Otherwise, it returns "Incorrect".
    """
    for key, value in sign_dict.items():
        if (independent1.find(key) >= 0 or key in independent1) and sign_encoder(param) == value:
            return "Correct"
    return "Incorrect"
                
def sign_encoder(number: float) -> bool:
    """
    If the number is less than zero, return -1, otherwise return 1
    
    :param number: the number to be encoded
    :return: The sign of the number.
    """
    if number < 0 :
        return -1
    else:
        return 1
