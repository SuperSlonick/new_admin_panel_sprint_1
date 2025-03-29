# sqlite_to_postgres/loader.py 
# читает данные из SQLite
from sqlite3 import Connection
from .models import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork


class SQLiteLoader:
    def __init__(self, conn: Connection):
        self.conn = conn

    def load_all(self) -> dict:
        return {
            'genre': self._load_table('genre', Genre),
            'person': self._load_table('person', Person),
            'film_work': self._load_table('film_work', FilmWork),
            'genre_film_work': self._load_table('genre_film_work', GenreFilmWork),
            'person_film_work': self._load_table('person_film_work', PersonFilmWork),
        }

    def _load_table(self, table_name, model_cls):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [model_cls(**dict(zip(columns, row))) for row in rows]