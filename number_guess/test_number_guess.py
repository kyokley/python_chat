import pytest
from number_guess.number_guess import intro, handle_response, InvalidInput


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
