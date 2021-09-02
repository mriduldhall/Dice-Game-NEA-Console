import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv("src/.env-vars")
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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games(
        id SERIAL PRIMARY KEY,
        player_one_id INTEGER REFERENCES users (id) ON DELETE set null,
        player_two_id INTEGER REFERENCES users (id) ON DELETE set null,
        player_one_score INTEGER NOT NULL,
        player_two_score INTEGER NOT NULL,
        winner INTEGER REFERENCES users (id) ON DELETE set null,
        game_end TIMESTAMP DEFAULT current_timestamp
        );
        """)
        connection.close()
    except OperationalError as error:
        print("The error", error, "occurred")
