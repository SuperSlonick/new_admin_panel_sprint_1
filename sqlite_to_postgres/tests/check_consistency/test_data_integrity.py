import sqlite3
import psycopg
from psycopg.rows import dict_row
from datetime import datetime
from uuid import UUID

SQLITE_PATH = 'db.sqlite'
POSTGRES_DSL = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': '127.0.0.1',
    'port': 5432,
}


TABLES = [
    'genre',
    'film_work',
    'person',
    'genre_film_work',
    'person_film_work',
]


def fetch_all_rows_sqlite(cursor, table):
    cursor.execute(f'SELECT * FROM {table}')
    return cursor.fetchall()


def fetch_all_rows_pg(cursor, table):
    cursor.execute(f'SELECT * FROM content.{table}')
    return cursor.fetchall()

def normalize_row(row: dict) -> dict:
    result = {}
    for k, v in row.items():
        if isinstance(v, datetime):
            result[k] = v.replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(v, UUID):
            result[k] = str(v)
        elif isinstance(v, str) and k.endswith('_at'):  # предполагаем, что это временное поле
            result[k] = v[:19]  # обрезаем до 'YYYY-MM-DD HH:MM:SS'
        else:
            result[k] = str(v) if v is not None else None
    return result

def test_tables_match():
    with sqlite3.connect(SQLITE_PATH) as sqlite_conn, psycopg.connect(**POSTGRES_DSL, row_factory=dict_row) as pg_conn:
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cur = sqlite_conn.cursor()
        pg_cur = pg_conn.cursor()

        for table in TABLES:
            sqlite_rows = fetch_all_rows_sqlite(sqlite_cur, table)
            pg_rows = fetch_all_rows_pg(pg_cur, table)

            assert len(sqlite_rows) == len(pg_rows), f"Row count mismatch in table '{table}'"

            sqlite_dicts = sorted([normalize_row(dict(row)) for row in sqlite_rows], key=lambda r: r['id'])
            pg_dicts = sorted([normalize_row(row) for row in pg_rows], key=lambda r: r['id'])

            for row_sqlite, row_pg in zip(sqlite_dicts, pg_dicts):
                assert row_sqlite == row_pg, f"Data mismatch in table '{table}' on ID {row_sqlite['id']}"
