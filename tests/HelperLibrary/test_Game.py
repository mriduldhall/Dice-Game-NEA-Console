import os
import pytest
import psycopg2
from unittest import mock
from psycopg2 import OperationalError
from src.HelperLibrary.Game import Game
from dotenv import load_dotenv, find_dotenv


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
    mock_object.side_effect = ["a", "a", "a", "a", "a"]
    game = Game("player1", "player2")
    game.player_one_score = player_one_score
    game.player_two_score = player_two_score
    winner = game.get_winner()
    if winner == game.player_one:
        assert game.player_one_score > game.player_two_score
    else:
        assert game.player_two_score > game.player_one_score


@pytest.mark.parametrize("player_one_name, player_two_name, winner", (
        ("Joe", "Tim", "Tim"),
        ("Joe", "Smith", "Joe")
))
def test_save(tables, player_one_name, player_two_name, winner):
    users_table, games_table = tables
    Game(player_one_name, player_two_name).save(winner, games_table, users_table)
