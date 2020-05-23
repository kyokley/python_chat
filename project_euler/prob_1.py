# Solution using aggregator
def sum_with_aggregator():
    sum_of_multiples = 0
    for i in range(1000):
        if i % 3 == 0 or i % 5 == 0:
            print(i)
            sum_of_multiples = i + sum_of_multiples

    print(sum_of_multiples)


# Solution with lists
def sum_with_lists():
    multiples = []
    for i in range(1000):
        if i % 3 == 0 or i % 5 == 0:
            multiples.append(i)
    print(multiples)
    print(sum(multiples))


# Solution using list comprehensions
def sum_with_list_comprehension():
    print(sum(i for i in range(1000) if i % 3 == 0 or i % 5 == 0))


if __name__ == '__main__':
    sum_with_lists()
