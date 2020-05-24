from number_guess.number_guess import intro


def test_intro(mocker):
    mocker.patch('number_guess.number_guess.time.sleep')
    intro()
