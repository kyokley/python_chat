import random
import time


LOWER = 'L'
HIGHER = 'H'
SPOT_ON = 'S'

ACCEPTABLE_RESPONSES = (LOWER,
                        HIGHER,
                        SPOT_ON)

INTRO_SLEEP_LENGTH = 10


class InvalidInput(Exception):
    pass


class NoValidGuessesRemaining(Exception):
    pass


def intro():
    print('Welcome to the Number Guessing Game!')
    print('Think of a number between 1-10')
    time.sleep(INTRO_SLEEP_LENGTH)


def main():
    lower_limit = 1
    upper_limit = 10

    intro()

    done = False
    while not done:
        try:
            resp, guess = make_guess(lower_limit, upper_limit)
        except NoValidGuessesRemaining:
            break

        if resp == SPOT_ON:
            print(f'We found your number! It was {guess}')
            done = True
        else:
            lower_limit, upper_limit = handle_response(resp, guess, lower_limit, upper_limit)


def make_guess(lower, upper):
    try:
        guess = random.randint(lower, upper)
    except (UnboundLocalError, ValueError):
        print("That's funny. I seem to have missed your number. Play again?")
        raise NoValidGuessesRemaining()

    print(f'Is your number {guess}?')

    resp = None
    while resp not in ACCEPTABLE_RESPONSES:
        resp = input('Enter L for lower, H for higher, S for spot on: ').upper().strip()
    return resp, guess


def handle_response(resp, current_guess, current_lower, current_upper):
    if resp == LOWER:
        # We need to shift our guesses lower
        new_lower = current_lower
        new_upper = current_guess - 1
    elif resp == HIGHER:
        # We need to shift our guesses higher
        new_lower = current_guess + 1
        new_upper = current_upper
    else:
        raise InvalidInput(f"Valid responses are 'L' or 'H'. Got '{resp}'")
    return new_lower, new_upper


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye!')
