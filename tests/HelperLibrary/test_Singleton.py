import pytest
from src.HelperLibrary.Singleton import Singleton


@pytest.fixture(autouse=True)
def reset():
    Singleton.reset()


def test_invalid_getinstance():
    with pytest.raises(Exception):
        Singleton.getinstance()


def test_valid_constructor():
    Singleton("", "")
    result = Singleton.getinstance()
    assert result is True


def test_invalid_constructor():
    with pytest.raises(Exception):
        Singleton("", "")
        Singleton("", "")


def test_values():
    singleton = Singleton("value1", "value2")
    assert singleton.player_one == "value1"
    assert singleton.player_two == "value2"
