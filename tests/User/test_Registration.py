import os
import pytest
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv, find_dotenv
from src.User.User import User
from src.User.Registration import Registration, RegistrationStore


@pytest.fixture(scope="module")
def resources():
    table_name = "testregistration"
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


@pytest.mark.parametrize("inputs, expected_result", (
        ("Joe", True),
        ("John", False),
))
def test_check_if_user_exists(table, inputs, expected_result):
    result = RegistrationStore(table).check_if_user_exists(inputs)
    assert result == expected_result


@pytest.mark.parametrize("username, password, expected_result", (
        ("John", "mypass123", [(4, 'John', 'mypass123')]),
))
def test_add_user(resources, username, password, expected_result):
    table, connection = resources
    user = User(username, password)
    RegistrationStore(table).add_user(user)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + table + " WHERE username='" + str(username) + "'")
    result = cursor.fetchall()
    assert result == expected_result


@pytest.mark.parametrize("username, password, expected_result", (
        ("John", "mypass123", "You have successfully created an account with the username John"),
        ("Smith", "mypass123", "Username is already taken"),
        ("Tim", "mypass123", "Username is already taken"),
))
def test_register(table, username, password, expected_result):
    user = User(username, password)
    result = Registration(table).register(user)
    assert result == expected_result
