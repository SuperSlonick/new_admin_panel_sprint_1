# sqlite_to_postgres/saver.py
# пишет данные в PostgreSQL
from psycopg import Connection
from typing import List
from dataclasses import asdict


class PostgresSaver:
    def __init__(self, conn: Connection):
        self.conn = conn

    def save_all(self, data: dict):
        with self.conn.cursor() as cur:
            for table, rows in data.items():
                if not rows:
                    continue
                columns = list(asdict(rows[0]).keys())
                values = [tuple(asdict(row).values()) for row in rows]

                placeholders = ', '.join(['%s'] * len(columns))
                column_list = ', '.join(columns)
                query = f"""
                    INSERT INTO content.{table} ({column_list})
                    VALUES ({placeholders})
                    ON CONFLICT (id) DO NOTHING
                """
                cur.executemany(query, values)
        self.conn.commit()