# sqlite_to_postgres/saver.py
# пишет данные в PostgreSQL пачками
from psycopg import Connection
from typing import Iterable
from dataclasses import asdict

class PostgresSaver:
    def __init__(self, conn: Connection):
        self.conn = conn

    def save_all(self, data: dict):
        with self.conn.cursor() as cur:
            for table, rows_iterator in data.items():
                for chunk in rows_iterator:
                    if not chunk:
                        continue

                    columns = list(asdict(chunk[0]).keys())
                    values = [tuple(asdict(row).values()) for row in chunk]

                    placeholders = ', '.join(['%s'] * len(columns))
                    column_list = ', '.join(columns)
                    query = f"""
                        INSERT INTO content.{table} ({column_list})
                        VALUES ({placeholders})
                        ON CONFLICT (id) DO NOTHING
                    """
                    cur.executemany(query, values)

        self.conn.commit()
