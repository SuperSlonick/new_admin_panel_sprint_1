from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class TimestampMixin:
    created_at: datetime = field(default_factory=datetime.now)
    
@dataclass
class Genre(TimestampMixin):
    id: str
    name: str
    description: Optional[str]
    updated_at: datetime


@dataclass
class FilmWork(TimestampMixin):
    id: str
    title: str
    description: Optional[str]
    creation_date: Optional[str]
    file_path: Optional[str]
    rating: Optional[float]
    type: str
    updated_at: datetime


@dataclass
class Person(TimestampMixin):
    id: str
    full_name: str
    updated_at: datetime


@dataclass
class GenreFilmWork(TimestampMixin):
    id: str
    film_work_id: str
    genre_id: str


@dataclass
class PersonFilmWork(TimestampMixin):
    id: str
    film_work_id: str
    person_id: str
    role: str
