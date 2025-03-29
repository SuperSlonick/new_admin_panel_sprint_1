from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Genre:
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class FilmWork:
    id: str
    title: str
    description: Optional[str]
    creation_date: Optional[str]
    file_path: Optional[str]
    rating: Optional[float]
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Person:
    id: str
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created_at: datetime


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime