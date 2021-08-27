import os
import pytest
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv, find_dotenv
from src.User.User import User
from src.User.Login import Login, LoginStore


@pytest.fixture(scope="module")
def resources():
    table_name = "testlogin"
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


@pytest.mark.parametrize("username, expected_result", (
        ("Joe", True),
        ("Smith", True),
        ("User", False)
))
def test_get_user_by_username(table, username, expected_result):
    user_result = LoginStore(table).get_user_by_username(username)
    result = isinstance(user_result, User)
    assert result == expected_result


@pytest.mark.parametrize("username, password, expected_result", (
        ("Joe", "mypass123", True),
        ("Smith", "mypass124", False),
        ("User", "password", False)
))
def test_login(table, username, password, expected_result):
    user = User(username, password)
    result = Login(table).login(user)
    assert result == expected_result
