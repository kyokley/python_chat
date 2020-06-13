def get_list(number):
    result = []

    for i in range(2, number + 1):  # 0, 1, 2, 3, ..., number
        result.append(i)

    return result


def remove_multiples(sequence, number):
    result = []

    for element in sequence:
        if element % number == 0 and element > number:
            # This is a multiple
            pass
        else:
            # This is not a multiple
            result.append(element)

    return result


def prime_list(number):
    long_list = get_list(number)

    idx = 0
    while idx < len(long_list):
        multiple_check = long_list[idx]
        long_list = remove_multiples(long_list, multiple_check)
        idx = idx + 1

    return long_list


# [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# [2, 3, 5, 7, 9, 11]
# [2, 3, 5, 7, 11]


# remove_multiples([2, 3, 4, 5, 6, 7, 8], 2) => [3, 5, 7]
# remove_multiples([2, 3, 4, 5, 6, 7, 8], 3) => [2, 4, 5, 7, 8]
# remove_multiples([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 4) => [2, 3, 5, 6, 7, 9, 10, 11]
