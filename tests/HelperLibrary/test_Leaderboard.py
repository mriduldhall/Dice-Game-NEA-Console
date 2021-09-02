import os
import pytest
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv, find_dotenv
from src.HelperLibrary.Leaderboard import Leaderboard


@pytest.fixture(scope='module')
def resources():
    users_table_name = "testusers"
    games_table_name = "testgames"
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


@pytest.fixture(autouse=True)
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
        games = [
            (1, 1, 2, 58, 29, 1),
            (2, 1, 2, 61, 56, 1),
            (3, 1, 2, 57, 63, 2),
            (4, 3, 2, 73, 94, 2),
            (5, 3, 2, 58, 55, 3),
            (6, 3, 1, 46, 63, 1),
            (7, 2, 1, 65, 91, 1),
            (8, 1, 3, 37, 82, 3),
            (9, 2, 3, 54, 47, 2),
            (10, 3, 2, 82, 58, 3)
        ]
        game_records = ", ".join(["%s"] * len(games))
        cursor.execute(
            f"INSERT INTO " + users_table_name + f"(id, username, password) VALUES {user_records}",
            users
        )
        cursor.execute(
            f"INSERT INTO " + games_table_name + f"(id, player_one_id, player_two_id, player_one_score, player_two_score, winner) VALUES {game_records}",
            games
        )
        cursor.execute("ALTER SEQUENCE " + users_table_name + "_id_seq RESTART WITH " + str(len(users)+1))
        cursor.execute("ALTER SEQUENCE " + games_table_name + "_id_seq RESTART WITH " + str(len(games)+1))
    except OperationalError as error:
        print("The error", error, "occurred")
    return users_table_name, games_table_name


def test_get_players(tables):
    users_table, games_table = tables
    records = Leaderboard(users_table, games_table).get_records()
    assert records == [[2, 94], [1, 91], [3, 82], [3, 82], [2, 63]]
