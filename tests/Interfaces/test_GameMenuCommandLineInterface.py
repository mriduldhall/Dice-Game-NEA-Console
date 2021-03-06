import os
import pytest
import psycopg2
from unittest import mock
from psycopg2 import OperationalError
from dotenv import load_dotenv, find_dotenv
from src.HelperLibrary.Singleton import Singleton
from src.Interfaces.GameMenuCommandLineInterface import CLI


@pytest.fixture(scope='module')
def resources():
    users_table_name = "users"
    games_table_name = "games"
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
            """CREATE TABLE IF NOT EXISTS """ + users_table_name + """ (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            )"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS """ + games_table_name + """(
            id SERIAL PRIMARY KEY,
            player_one_id INTEGER REFERENCES """ + users_table_name + """ (id) ON DELETE set null,
            player_two_id INTEGER REFERENCES """ + users_table_name + """ (id) ON DELETE set null,
            player_one_score INTEGER NOT NULL,
            player_two_score INTEGER NOT NULL,
            winner INTEGER REFERENCES """ + users_table_name + """ (id) ON DELETE set null,
            game_end TIMESTAMP DEFAULT current_timestamp
            )"""
        )
    except OperationalError as error:
        print("The error", error, "occurred")
    yield users_table_name, games_table_name, connection
    try:
        cursor.execute(
            """DROP TABLE IF EXISTS """ + games_table_name
        )
        cursor.execute(
            """DROP TABLE IF EXISTS """ + users_table_name
        )
        connection.close()
    except OperationalError as error:
        print("The error", error, "occurred")


@pytest.fixture()
def tables(resources):
    users_table_name, games_table_name, connection = resources
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(
            """DELETE FROM """ + games_table_name
        )
        cursor.execute(
            """DELETE FROM """ + users_table_name
        )
        users = [
            (1, "Joe", "mypass123"),
            (2, "Tim", "test1ng"),
            (3, "Smith", "mypass123")
        ]
        user_records = ", ".join(["%s"] * len(users))
        cursor.execute(
            f"INSERT INTO " + users_table_name + f"(id, username, password) VALUES {user_records}",
            users
        )
        cursor.execute("ALTER SEQUENCE " + users_table_name + "_id_seq RESTART WITH " + str(len(users)+1))
        cursor.execute("ALTER SEQUENCE " + games_table_name + "_id_seq RESTART WITH 1")
    except OperationalError as error:
        print("The error", error, "occurred")
    return users_table_name, games_table_name


@pytest.fixture(autouse=True)
def reset():
    Singleton.reset()


@pytest.mark.parametrize('inputs', (
    # Leaderboard and capitalisation
    ["l", "E"],
))
@mock.patch('builtins.input')
def test_CLI(mock_object, tables, inputs):
    mock_object.side_effect = inputs
    CLI(Singleton("", "")).initiate()
