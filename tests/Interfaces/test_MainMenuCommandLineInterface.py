import os
import pytest
import psycopg2
from unittest import mock
from src.User.User import User
from psycopg2 import OperationalError
from dotenv import load_dotenv, find_dotenv
from src.HelperLibrary.Singleton import Singleton
from src.Interfaces.MainMenuCommandLineInterface import CLI, RegisterMenuItem


@pytest.fixture(autouse=True)
def reset():
    Singleton.reset()


@pytest.fixture(scope="module")
def resources():
    table_name = "users"
    load_dotenv(find_dotenv(".env-vars"))
    connection = psycopg2.connect(
        database=os.getenv("name"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
    )
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS """ + table_name + """ (
            id SERIAL PRIMARY KEY, 
            username TEXT NOT NULL, 
            password TEXT NOT NULL
            )"""
        )
    except OperationalError as error:
        print("The error", error, "occurred")
    yield table_name, connection
    try:
        cursor.execute(
            """DROP TABLE IF EXISTS """ + table_name
        )
        connection.close()
    except OperationalError as error:
        print("The error", error, "occurred")


@pytest.fixture(autouse=True)
def table(resources):
    table_name, connection = resources
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(
            """DELETE FROM """ + table_name
        )
        users = [
            (1, "Joe", "mypass123"),
            (2, "Tim", "test1ng"),
            (3, "Smith", "mypass123")
        ]
        user_records = ", ".join(["%s"] * len(users))
        cursor.execute(
            f"INSERT INTO " + table_name + f"(id, username, password) VALUES {user_records}",
            users
        )
        cursor.execute("ALTER SEQUENCE " + table_name + "_id_seq RESTART WITH " + str(len(users)+1))
    except OperationalError as error:
        print("The error", error, "occurred")
    return table_name


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


@pytest.mark.parametrize('inputs', (
    # Information and capitalisation
    ["i", "E"],
    # Validator
    ["l", "0", "l", "1", "user", "password", "0", "e"],
    # Valid register
    ["r", "1", "user", "mypass123", "e"],
    # Login try again
    ["l", "0", "l", "1", "User", "password", "0", "e"],
    # Invalid register followed by valid login
    ["r", "1", "tim", "test1ng", "l", "1", "Tim", "test1ng", "smith", "mypass123", "e", "e"],
    # Valid login and try again
    ["l", "1", "joe", "mypass123", "Tim", "testing", "1", "Tim", "test1ng", "e", "e"]
))
@mock.patch('builtins.input')
def test_CLI(mock_object, inputs):
    mock_object.side_effect = inputs
    CLI().initiate()
