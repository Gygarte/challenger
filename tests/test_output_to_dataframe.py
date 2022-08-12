from challenger.algo import add_output_to_dataframe


def test_output_to_dataframe():
    import random
    import string

    for index in range(10):
        letter_1 = random.choice(string.ascii_letters)
        letter_2 = random.choice(string.ascii_letters)
        output_of_processing = [{"Independent_1": f"{letter_1}",
                                 "Independent_2": f"{letter_2}",
                                 "Independent_1_coef": random.randint(-100, 100),
                                 "Independent_2_coef": random.randint(-100, 100)} for i in range(3)]
        sign_dict = {f"{letter_1}": random.choice((-1, 1)),
                     f"{letter_2}": random.choice((-1, 1))}
        type_of_model = 2
        result = add_output_to_dataframe.output_to_dataframe(output_of_processing, sign_dict, type_of_model)
        print(result.head())


if __name__ == "__main__":
    test_output_to_dataframe()
