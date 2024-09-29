CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    login varchar(50) UNIQUE,
    password varchar(255) NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name varchar(50),
    author varchar(100)
);

CREATE TABLE sharing (
    owner integer references Users(id) on DELETE CASCADE,
    book integer references books(id) on DELETE CASCADE
);

CREATE TABLE requests (
    id serial primary key,
    requester integer references Users(id) on DELETE CASCADE,
    owner integer references Users(id) on DELETE CASCADE,
    book integer references books(id) on DELETE CASCADE,
    is_accepted bool
);
