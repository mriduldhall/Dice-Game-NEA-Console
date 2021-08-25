from src.HelperLibrary.StorageFunctions import StorageFunctions
import os
import pytest
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope='module')
def resources(table_name="storage_functions_test"):
    def database_reset():
        cursor.execute(
            """DELETE FROM """ + table_name
        )
        users = [
            (1, "Joe", "pass!", 39, True),
            (2, "Tim", "test1ng", 47, False),
            (3, "John", "john", 18, False),
            (4, "Smith", "qwerty", 74, True),
            (5, "James", "1234", 28, True)
        ]
        user_records = ", ".join(["%s"] * len(users))
        cursor.execute(
            f"INSERT INTO " + table_name + f"(id, username, password, age, active) VALUES {user_records}",
            users
        )
        return database_reset

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
            password TEXT NOT NULL,
            age INT NOT NULL,
            active BOOLEAN NOT NULL 
            )"""
        )
        database_reset()
    except OperationalError as error:
        print("The error", error, "occurred")
    yield table_name, database_reset
    try:
        cursor.execute(
            """DROP TABLE IF EXISTS """ + table_name
        )
        connection.close()
    except OperationalError as error:
        print("The error", error, "occurred")


@pytest.fixture(autouse=True)
def storage_object(resources):
    table_name, database_reset = resources
    database_reset()
    load_dotenv(find_dotenv(".env-vars"))
    storage_object = StorageFunctions(
        table_name=table_name,
        db_name=os.getenv("name"),
        db_user=os.getenv("user"),
        db_password=os.getenv("password"),
        db_host=os.getenv("host"),
        db_port=os.getenv("port"),
    )
    return storage_object


def test_constructor(storage_object):
    assert isinstance(storage_object, StorageFunctions)
    assert storage_object.connection is not None


def test_append(storage_object):
    storage_object.append("(id, username, password, age, active)", [6, "Robert", "password", 54, True])
    storage_object.connection.autocommit = True
    cursor = storage_object.connection.cursor()
    cursor.execute("""SELECT * FROM """ + storage_object.table + " WHERE username = 'Robert'")
    record = cursor.fetchone()
    assert record[1] == "Robert"


def test_list(storage_object):
    records = storage_object.list("username")
    assert len(records) == 5
    assert records == ["Joe", "Tim", "John", "Smith", "James"]


@pytest.mark.parametrize("column_list, data_list, negative, expected_result", [
    (["active"], [True], False, [(1, 'Joe', 'pass!', 39, True), (4, 'Smith', 'qwerty', 74, True), (5, 'James', '1234', 28, True)]),
    (["active"], [True], True, [(2, 'Tim', 'test1ng', 47, False), (3, 'John', 'john', 18, False)]),
    (["username", "age"], ["Smith", 74], False, [(4, 'Smith', 'qwerty', 74, True)])
])
def test_retrieve(storage_object, column_list, data_list, negative, expected_result):
    result = storage_object.retrieve(column_list, data_list, negative)
    assert result == expected_result


@pytest.mark.parametrize("column_list, data_list, identifier_value, identifier, test_query, expected_result", [
    (["active"], [False], 1, "id", """SELECT * FROM storage_functions_test WHERE id = 1""", [(1, 'Joe', 'pass!', 39, False)]),
    (["active"], [False], "James", "username", """SELECT * FROM storage_functions_test WHERE username = 'James'""", [(5, 'James', '1234', 28, False)]),
    (["password", "age"], ["temp", 48], 2, "id", """SELECT * FROM storage_functions_test WHERE id = 2""", [(2, 'Tim', 'temp', 48, False)]),
    (["active"], [True], False, "active", """SELECT * FROM storage_functions_test""", [(1, 'Joe', 'pass!', 39, True), (4, 'Smith', 'qwerty', 74, True), (5, 'James', '1234', 28, True), (2, 'Tim', 'test1ng', 47, True), (3, 'John', 'john', 18, True)])
])
def test_update(storage_object, column_list, data_list, identifier_value, identifier, test_query, expected_result):
    storage_object.update(column_list, data_list, identifier_value, identifier)
    storage_object.connection.autocommit = True
    cursor = storage_object.connection.cursor()
    cursor.execute(test_query)
    records = cursor.fetchall()
    assert records == expected_result


@pytest.mark.parametrize("data, identifier, test_query, expected_result", [
    (1, "id", """SELECT * FROM storage_functions_test WHERE id = 1""", []),
    ("Tim", "username", """SELECT * FROM storage_functions_test WHERE username = 'Tim'""", []),
    (False, "active", """SELECT * FROM storage_functions_test WHERE active = False""", [])
])
def test_delete(storage_object, data, identifier, test_query, expected_result):
    storage_object.delete(data, identifier)
    storage_object.connection.autocommit = True
    cursor = storage_object.connection.cursor()
    cursor.execute(test_query)
    records = cursor.fetchall()
    assert records == expected_result
