DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS task CASCADE;
DROP TABLE IF EXISTS project CASCADE;
DROP TABLE IF EXISTS team CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS userteam CASCADE;
DROP TABLE IF EXISTS userprofile CASCADE;


create table task
(
    name        varchar not null,
    description varchar,
    deadline    timestamp,
    id          serial
        primary key,
    project_id  integer not null
);

INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 1', 'Description for Task 1', '2024-06-10 12:00:00', 1);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 2', 'Description for Task 2', '2024-06-11 12:00:00', 1);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 3', 'Description for Task 3', '2024-06-12 12:00:00', 2);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 4', 'Description for Task 4', '2024-06-13 12:00:00', 2);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 5', 'Description for Task 5', '2024-06-14 12:00:00', 3);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 6', 'Description for Task 6', '2024-06-15 12:00:00', 3);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 7', 'Description for Task 7', '2024-06-16 12:00:00', 4);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 8', 'Description for Task 8', '2024-06-17 12:00:00', 4);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 9', 'Description for Task 9', '2024-06-18 12:00:00', 5);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 10', 'Description for Task 10', '2024-06-19 12:00:00', 5);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 11', 'Description for Task 11', '2024-06-20 12:00:00', 6);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 12', 'Description for Task 12', '2024-06-21 12:00:00', 6);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 13', 'Description for Task 13', '2024-06-22 12:00:00', 7);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 14', 'Description for Task 14', '2024-06-23 12:00:00', 7);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 15', 'Description for Task 15', '2024-06-24 12:00:00', 8);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 16', 'Description for Task 16', '2024-06-25 12:00:00', 8);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 17', 'Description for Task 17', '2024-06-26 12:00:00', 9);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 18', 'Description for Task 18', '2024-06-27 12:00:00', 9);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 19', 'Description for Task 19', '2024-06-28 12:00:00', 10);
INSERT INTO task (name, description, deadline, project_id) VALUES ('Task 20', 'Description for Task 20', '2024-06-29 12:00:00', 10);

create table team (
    id   serial primary key,
    name varchar not null
);

INSERT INTO team (name) VALUES ('Team 1');
INSERT INTO team (name) VALUES ('Team 2');
INSERT INTO team (name) VALUES ('Team 3');
INSERT INTO team (name) VALUES ('Team 4');
INSERT INTO team (name) VALUES ('Team 5');
INSERT INTO team (name) VALUES ('Team 6');
INSERT INTO team (name) VALUES ('Team 7');
INSERT INTO team (name) VALUES ('Team 8');
INSERT INTO team (name) VALUES ('Team 9');
INSERT INTO team (name) VALUES ('Team 10');
INSERT INTO team (name) VALUES ('Team 11');
INSERT INTO team (name) VALUES ('Team 12');
INSERT INTO team (name) VALUES ('Team 13');
INSERT INTO team (name) VALUES ('Team 14');
INSERT INTO team (name) VALUES ('Team 15');
INSERT INTO team (name) VALUES ('Team 16');
INSERT INTO team (name) VALUES ('Team 17');
INSERT INTO team (name) VALUES ('Team 18');
INSERT INTO team (name) VALUES ('Team 19');
INSERT INTO team (name) VALUES ('Team 20');

create table "user"
(
    id         serial  primary key,
    username   varchar not null,
    password   varchar not null,
    profile_id integer
);

INSERT INTO "user" (username, password, profile_id) VALUES ('user1', 'password1', 1);
INSERT INTO "user" (username, password, profile_id) VALUES ('user2', 'password2', 2);
INSERT INTO "user" (username, password, profile_id) VALUES ('user3', 'password3', 3);
INSERT INTO "user" (username, password, profile_id) VALUES ('user4', 'password4', 4);
INSERT INTO "user" (username, password, profile_id) VALUES ('user5', 'password5', 5);
INSERT INTO "user" (username, password, profile_id) VALUES ('user6', 'password6', 6);
INSERT INTO "user" (username, password, profile_id) VALUES ('user7', 'password7', 7);
INSERT INTO "user" (username, password, profile_id) VALUES ('user8', 'password8', 8);
INSERT INTO "user" (username, password, profile_id) VALUES ('user9', 'password9', 9);
INSERT INTO "user" (username, password, profile_id) VALUES ('user10', 'password10', 10);
INSERT INTO "user" (username, password, profile_id) VALUES ('user11', 'password11', 11);
INSERT INTO "user" (username, password, profile_id) VALUES ('user12', 'password12', 12);
INSERT INTO "user" (username, password, profile_id) VALUES ('user13', 'password13', 13);
INSERT INTO "user" (username, password, profile_id) VALUES ('user14', 'password14', 14);
INSERT INTO "user" (username, password, profile_id) VALUES ('user15', 'password15', 15);
INSERT INTO "user" (username, password, profile_id) VALUES ('user16', 'password16', 16);
INSERT INTO "user" (username, password, profile_id) VALUES ('user17', 'password17', 17);
INSERT INTO "user" (username, password, profile_id) VALUES ('user18', 'password18', 18);
INSERT INTO "user" (username, password, profile_id) VALUES ('user19', 'password19', 19);
INSERT INTO "user" (username, password, profile_id) VALUES ('user20', 'password20', 20);

create table userprofile
(
    id         serial primary key,
    avatar     varchar,
    birth_date varchar,
    skills     json not null
);

INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar1.jpg', '1990-01-01', '{"skill1": "Programming", "skill2": "Design"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar2.jpg', '1991-02-02', '{"skill1": "Marketing", "skill2": "Communication"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar3.jpg', '1992-03-03', '{"skill1": "Data Analysis", "skill2": "Problem Solving"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar4.jpg', '1993-04-04', '{"skill1": "Project Management", "skill2": "Leadership"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar5.jpg', '1994-05-05', '{"skill1": "Writing", "skill2": "Content Creation"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar6.jpg', '1995-06-06', '{"skill1": "Customer Service", "skill2": "Sales"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar7.jpg', '1996-07-07', '{"skill1": "Finance", "skill2": "Accounting"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar8.jpg', '1997-08-08', '{"skill1": "Human Resources", "skill2": "Recruitment"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar9.jpg', '1998-09-09', '{"skill1": "Networking", "skill2": "Social Media"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar10.jpg', '1999-10-10', '{"skill1": "Education", "skill2": "Teaching"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar11.jpg', '2000-11-11', '{"skill1": "Healthcare", "skill2": "Nursing"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar12.jpg', '2001-12-12', '{"skill1": "Art", "skill2": "Creativity"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar13.jpg', '2002-01-13', '{"skill1": "Engineering", "skill2": "Innovation"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar14.jpg', '2003-02-14', '{"skill1": "Research", "skill2": "Analysis"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar15.jpg', '2004-03-15', '{"skill1": "Law", "skill2": "Legal"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar16.jpg', '2005-04-16', '{"skill1": "Consulting", "skill2": "Advisory"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar17.jpg', '2006-05-17', '{"skill1": "Architecture", "skill2": "Design"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar18.jpg', '2007-06-18', '{"skill1": "Science", "skill2": "Research"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar19.jpg', '2008-07-19', '{"skill1": "Entertainment", "skill2": "Performance"}');
INSERT INTO userprofile (avatar, birth_date, skills) VALUES ('avatar20.jpg', '2009-08-20', '{"skill1": "Environment", "skill2": "Sustainability"}');

create table userteam
(
    team_id  integer,
    user_id  integer,
    position varchar not null,
    primary key (team_id, user_id)
);

INSERT INTO userteam (team_id, user_id, position) VALUES (1, 1, 'Leader');
INSERT INTO userteam (team_id, user_id, position) VALUES (1, 2, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (1, 3, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (1, 4, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (1, 5, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (2, 6, 'Leader');
INSERT INTO userteam (team_id, user_id, position) VALUES (2, 7, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (2, 8, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (2, 9, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (2, 10, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (3, 11, 'Leader');
INSERT INTO userteam (team_id, user_id, position) VALUES (3, 12, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (3, 13, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (3, 14, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (3, 15, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (4, 16, 'Leader');
INSERT INTO userteam (team_id, user_id, position) VALUES (4, 17, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (4, 18, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (4, 19, 'Member');
INSERT INTO userteam (team_id, user_id, position) VALUES (4, 20, 'Member');

create table project
(
    id              serial primary key,
    name            varchar not null,
    description     varchar,
    expected_result varchar,
    team_id         integer not null
);

INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 1', 'Description for project 1', 'Expected result 1', 1);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 2', 'Description for project 2', 'Expected result 2', 2);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 3', 'Description for project 3', 'Expected result 3', 3);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 4', 'Description for project 4', 'Expected result 4', 4);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 5', 'Description for project 5', 'Expected result 5', 5);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 6', 'Description for project 6', 'Expected result 6', 1);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 7', 'Description for project 7', 'Expected result 7', 2);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 8', 'Description for project 8', 'Expected result 8', 3);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 9', 'Description for project 9', 'Expected result 9', 4);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 10', 'Description for project 10', 'Expected result 10', 5);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 11', 'Description for project 11', 'Expected result 11', 1);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 12', 'Description for project 12', 'Expected result 12', 2);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 13', 'Description for project 13', 'Expected result 13', 3);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 14', 'Description for project 14', 'Expected result 14', 4);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 15', 'Description for project 15', 'Expected result 15', 5);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 16', 'Description for project 16', 'Expected result 16', 1);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 17', 'Description for project 17', 'Expected result 17', 2);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 18', 'Description for project 18', 'Expected result 18', 3);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 19', 'Description for project 19', 'Expected result 19', 4);
INSERT INTO project (name, description, expected_result, team_id) VALUES ('Project 20', 'Description for project 20', 'Expected result 20', 5);
