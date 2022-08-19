from typing import Union


def sign_filter(sign_dict: dict, model_coef: Union[list, tuple], indep_var_combination: Union[list, tuple]) -> list:
    def _encode_coef_sign(coef: float) -> int:
        return -1 if coef < 0 else 1

    result = []
    for var, sign in sign_dict.items():
        for index, variable in enumerate(indep_var_combination):
            if var in variable:
                print(f"var: {var}")
                print(f"varaible:{variable}")
                if _encode_coef_sign(model_coef[index]) == sign:
                    result.append("Correct!")
                    print(result)
                else:
                    result.append("Incorrect!")
                    print(result)
            else:
                result.append("Not provided")
                print(result)
    return result
