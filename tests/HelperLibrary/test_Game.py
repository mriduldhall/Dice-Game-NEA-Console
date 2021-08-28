import pytest
from unittest import mock
from src.HelperLibrary.Game import Game


@pytest.mark.parametrize('execution_number', range(6))
def test_roll_die(execution_number):
    roll = Game(None, None).roll_dice()
    assert 0 < roll < 7


@pytest.mark.parametrize("roll_one, roll_two, current_score, expected_score", (
        (1, 3, 0, 14),
        (2, 6, 3, 21),
        (5, 4, 28, 32),
        (1, 2, 0, 0)
))
def test_calculate_score(roll_one, roll_two, current_score, expected_score):
    new_score = Game(None, None).calculate_score(roll_one, roll_two, current_score)
    assert new_score == expected_score


@pytest.mark.parametrize("roll_one, roll_two, current_score, minimum_score, maximum_score", (
        (1, 1, 0, 13, 18),
        (5, 5, 37, 58, 63)
))
def test_calculate_score_with_double(roll_one, roll_two, current_score, minimum_score, maximum_score):
    new_score = Game(None, None).calculate_score(roll_one, roll_two, current_score)
    assert minimum_score <= new_score <= maximum_score


@pytest.mark.parametrize("player_one_score, player_two_score", (
        (3, 5),
        (0, 0),
        (82, 73),
        (36, 36)
))
@mock.patch('builtins.input')
def test_get_winner(mock_object, player_one_score, player_two_score):
    mock_object.side_effect = "a"
    game = Game("player1", "player2")
    game.player_one_score = player_one_score
    game.player_two_score = player_two_score
    winner = game.get_winner()
    if winner == game.player_one:
        assert game.player_one_score > game.player_two_score
    else:
        assert game.player_two_score > game.player_one_score
