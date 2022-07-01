from itertools import combinations


def create_variable_combinations(list_of_var: list, number_of_var_for_combination: int, sign_dictionary: dict) -> list:
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
