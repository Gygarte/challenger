def test_create_variable_combinations(results):
    counter_group = 0
    for group in results:

        # special case

        if len(group) == 1:

            counter_group += 1
        else:

            counter_item = 0
            for index, item in enumerate(group):
                # print("Current item is {}".format(item))
                ref_pos = index + 1
                # print("Current ref_pos is {}".format(ref_pos))
                if ref_pos > len(group):
                    counter_item += 1
                else:
                    while ref_pos <= len(group):
                        # print("current ref_pos in while is {}".format(ref_pos))
                        if ref_pos >= len(group):
                            counter_item += 1
                            # print("Current counter_item is {}".format(counter_item))
                            break
                        if item in group[ref_pos]:
                            # print("Found a fail!")
                            break
                        ref_pos += 1

            if counter_item == len(group):
                counter_group += 1
    if counter_group == len(results):
        return "Passed, for all groups!"
    else:
        return "Failed!"