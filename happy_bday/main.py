import time
import sys
from random import SystemRandom
from blessings import Terminal

TERM = Terminal()
RAND = SystemRandom()
DEFAULT_STEP_TIME = .15
INITIAL_LOCATION = (5, 5)
ITERATIONS = 10


def main(msg):
    print(TERM.clear())
    while True:
        display_random(msg)
        time.sleep(DEFAULT_STEP_TIME)

        if RAND.choice([True, False]):
            print(TERM.clear())


def inline_print(msg):
    print(msg, end='')


def display_random(msg, step_time=DEFAULT_STEP_TIME):
    funcs = [str.upper,
             str.lower,
             lambda x: x]

    new_msg = ''
    for char in msg:
        func = RAND.choice(funcs)
        new_msg += func(char)

    with TERM.location(*INITIAL_LOCATION):
        for char in new_msg:
            color_int = RAND.randint(1, 14)
            inline_print(TERM.color(color_int) + char + TERM.normal)
            time.sleep(step_time)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        pass
