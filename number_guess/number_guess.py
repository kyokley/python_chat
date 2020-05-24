import random
import time


class InvalidInput(Exception):
    pass


def intro():
    print('Welcome to the Number Guessing Game!')
    print('Think of a number between 1-10')
    time.sleep(2)


def main():
    lower_limit = 1
    upper_limit = 10

    intro()

    done = False
    while not done:
        resp, guess = make_guess(lower_limit, upper_limit)

        if resp == 'S':
            print('We found your number! It was {}'.format(guess))
            done = True
        else:
            lower_limit, upper_limit = handle_response(resp, guess, lower_limit, upper_limit)


def make_guess(lower, upper):
    guess = random.randint(lower, upper)
    print('Is your number {}?'.format(guess))

    resp = input('Enter L for lower, H for higher, S for spot on: ').upper().strip()
    return resp, guess


def handle_response(resp, current_guess, current_lower, current_upper):
    if resp == 'L':
        # We need to shift our guesses lower
        new_lower = current_lower
        new_upper = current_guess - 1
    elif resp == 'H':
        # We need to shift our guesses higher
        new_lower = current_guess + 1
        new_upper = current_upper
    else:
        raise InvalidInput(f"Valid responses are 'L' or 'H'. Got '{resp}'")
    return new_lower, new_upper


if __name__ == '__main__':
    main()
