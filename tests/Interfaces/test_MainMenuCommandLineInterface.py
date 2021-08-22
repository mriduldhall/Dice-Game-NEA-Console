import pytest
from unittest import mock
from src.User.User import User
from src.Interfaces.MainMenuCommandLineInterface import RegisterMenuItem


@pytest.mark.parametrize('username, password', (
    ["Mark", "P@ssword123!"],
    ["tim", "mypass"],
))
@mock.patch('builtins.input')
def test_get_new_user_details(mock_object, username, password):
    mock_object.side_effect = [username, password]
    user = RegisterMenuItem()._get_new_user_details()
    assert isinstance(user, User)
    assert user.username == username.capitalize()
    assert user.password == password
