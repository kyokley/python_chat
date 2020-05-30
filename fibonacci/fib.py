# n =  1  2  3  4  5  6   7
#             |
#             v
# fibs 1, 1, 2, 3, 5, 8, 13, ...

# fibs(4) => 3
# fibs(7) => 13


def fib(n):
    print(n)
    if n < 1:
        print('n cannot be less than one!')
        return
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def bad(n):
    print(n)
    return bad(n - 1)
