import pytest
from unittest import mock
from src.HelperLibrary.Validator import Validator


@pytest.mark.parametrize("inputs, expected_result", (
    [[True, "one", 1, "1"], True],
    [[3, -3, "0"], False]
))
@mock.patch('builtins.input')
def test_validator(mock_object, inputs, expected_result):
    mock_object.side_effect = inputs
    response = Validator("test").should_continue()
    assert response == expected_result
