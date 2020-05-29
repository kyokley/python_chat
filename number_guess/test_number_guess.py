import pytest
from number_guess.number_guess import (intro,
                                       handle_response,
                                       InvalidInput,
                                       HIGHER,
                                       make_guess,
                                       LOWER,
                                       SPOT_ON,
                                       NoValidGuessesRemaining,
                                       )


def test_intro(mocker):
    mocker.patch('number_guess.number_guess.time.sleep')
    intro()


class TestHandleResponse:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.current_lower = 1
        self.current_upper = 10
        self.test_guess = 5

    def test_resp_lower(self):
        """Test where target number is lower than the last guess."""
        self.test_guess = 5

        expected_lower = 1
        expected_upper = 4

        actual_lower, actual_upper = handle_response('L',
                                                     self.test_guess,
                                                     self.current_lower,
                                                     self.current_upper)

        assert expected_lower == actual_lower
        assert expected_upper == actual_upper

    def test_resp_higher(self):
        """Test where target number is higher than the last guess."""
        self.test_guess = 5

        expected_lower = 6
        expected_upper = 10

        actual_lower, actual_upper = handle_response('H',
                                                     self.test_guess,
                                                     self.current_lower,
                                                     self.current_upper)

        assert expected_lower == actual_lower
        assert expected_upper == actual_upper

    def test_invalid(self):
        with pytest.raises(InvalidInput):
            handle_response('asdf',
                            self.test_guess,
                            self.current_lower,
                            self.current_upper)


class TestMakeGuess:
    @pytest.fixture(autouse=True)
    def setUp(self, mocker):
        self.mock_input = mocker.patch('number_guess.number_guess.input')
        self.mock_input.return_value = HIGHER

    @pytest.mark.parametrize('user_resp',
                             [HIGHER, LOWER, SPOT_ON])
    def test_valid_range(self, user_resp):
        self.mock_input.return_value = user_resp
        lower = 3
        upper = 7

        actual_resp, actual_guess = make_guess(lower, upper)
        assert actual_resp == user_resp
        assert lower <= actual_guess <= upper

    @pytest.mark.parametrize('lower,upper',
                             [(1, 0),
                              (11, 10),
                              ])
    def test_invalid_range(self, lower, upper):
        with pytest.raises(NoValidGuessesRemaining):
            make_guess(lower, upper)
