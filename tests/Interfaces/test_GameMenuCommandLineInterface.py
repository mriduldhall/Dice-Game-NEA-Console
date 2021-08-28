import pytest
from unittest import mock
from src.HelperLibrary.Singleton import Singleton
from src.Interfaces.GameMenuCommandLineInterface import CLI


@pytest.fixture(autouse=True)
def reset():
    Singleton.reset()


@pytest.mark.parametrize('inputs', (
    # Leaderboard and capitalisation
    ["l", "E"],
))
@mock.patch('builtins.input')
def test_CLI(mock_object, inputs):
    mock_object.side_effect = inputs
    CLI(Singleton("", "")).initiate()
