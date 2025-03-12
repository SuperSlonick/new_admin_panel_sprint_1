CREATE SCHEMA content;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE content.genre (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP DEFAULT NOW(),
    modified TIMESTAMP DEFAULT NOW()
);

CREATE TABLE content.film_work (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating NUMERIC(3,1),
    type TEXT NOT NULL,
    created TIMESTAMP DEFAULT NOW(),
    modified TIMESTAMP DEFAULT NOW()
);

CREATE TABLE content.person (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    created TIMESTAMP DEFAULT NOW(),
    modified TIMESTAMP DEFAULT NOW()
);

CREATE TABLE content.genre_film_work (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    genre_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    created TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    UNIQUE (genre_id, film_work_id)
);

CREATE TABLE content.person_film_work (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    role TEXT NOT NULL,
    created TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    UNIQUE (person_id, film_work_id, role)
);

-- Индексы 
CREATE INDEX idx_film_work_creation_date ON content.film_work (creation_date);
CREATE INDEX idx_film_work_rating ON content.film_work (rating);
CREATE INDEX idx_person_full_name ON content.person (full_name);
CREATE INDEX idx_genre_name ON content.genre (name);
