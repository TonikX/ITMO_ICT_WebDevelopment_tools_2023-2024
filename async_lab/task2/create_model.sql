create table task
(
    name        varchar not null,
    description varchar,
    deadline    timestamp,
    id          serial
        primary key,
    project_id  integer not null
);