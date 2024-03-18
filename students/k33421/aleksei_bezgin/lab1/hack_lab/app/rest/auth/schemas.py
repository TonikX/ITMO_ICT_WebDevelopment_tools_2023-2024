import datetime

from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class Hackathon(SQLModel):
    id: int
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class Team(SQLModel):
    id: int
    name: str
    hackathon: Hackathon
    role: str


class User(SQLModel):
    id: int
    username: str
    email: str | None = None
    full_name: str | None = None
    contact_number: str | None

    teams: list[Team] | None = None


class UserCreateData(SQLModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None
    contact_number: str | None


class UserPassword(SQLModel):
    password: str