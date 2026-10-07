-- Pasos 4, 5 y 6: modelo normalizado (E/R) en PostgreSQL (Data Warehouse)

CREATE TABLE species (
    species_id SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE location (
    location_id INT PRIMARY KEY,          -- id sacado de la URL de la API
    name        VARCHAR(150) NOT NULL,
    url         VARCHAR(255)
);

CREATE TABLE episode (
    episode_id INT PRIMARY KEY            -- id sacado de la URL del episodio
);

CREATE TABLE character (
    character_id INT PRIMARY KEY,
    name         VARCHAR(150) NOT NULL,
    status       VARCHAR(20)  CHECK (status IN ('Alive','Dead','unknown')),
    species_id   INT REFERENCES species(species_id),
    type         VARCHAR(150),
    gender       VARCHAR(20)  CHECK (gender IN ('Female','Male','Genderless','unknown')),
    origin_id    INT REFERENCES location(location_id),
    location_id  INT REFERENCES location(location_id),
    image        VARCHAR(255),
    created      TIMESTAMP
);

-- Relación N:M personaje <-> episodio
CREATE TABLE character_episode (
    character_id INT REFERENCES character(character_id),
    episode_id   INT REFERENCES episode(episode_id),
    PRIMARY KEY (character_id, episode_id)
);
