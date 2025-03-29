# load_data.py

import sqlite3
import psycopg
from psycopg.rows import dict_row
from psycopg import ClientCursor, connection as _connection

from sqlite_to_postgres.loader import SQLiteLoader
from sqlite_to_postgres.saver import PostgresSaver


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    loader = SQLiteLoader(sqlite_conn)
    saver = PostgresSaver(pg_conn)
    data = loader.load_all()
    saver.save_all(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg.connect(**dsl, row_factory=dict_row, cursor_factory=ClientCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)