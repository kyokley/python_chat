import pytest
from sieve_of_eratosthenes.sieve import prime_list


def test_primes_list_10():
    expected = [2, 3, 5, 7]
    actual = prime_list(10)

    assert expected == actual


def test_primes_list_105():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23,
                29, 31, 37, 41, 43, 47, 53, 59,
                61, 67, 71, 73, 79, 83, 89, 97,
                101, 103]
    actual = prime_list(105)

    assert expected == actual


def test_negative_number_is_invalid_input():
    with pytest.raises(Exception):
        prime_list(-10)


def test_non_int_is_invalid_input():
    with pytest.raises(Exception):
        prime_list('w')

    with pytest.raises(Exception):
        prime_list(2.5)
