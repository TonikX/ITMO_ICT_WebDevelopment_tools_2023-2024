import datetime

from sqlmodel import SQLModel


class Team(SQLModel):
    id: int
    name: str


class Task(SQLModel):
    id: int
    title: str
    description: str
    requirements: str
    evaluation_criteria: str


class Hackathon(SQLModel):
    id: int | None
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime

    tasks: list[Task]
    teams: list[Team]


class HackathonCreateData(SQLModel):
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class HackathonUpdateData(SQLModel):
    name: str | None = None
    start_date: datetime.datetime | None = None
    end_date: datetime.datetime | None = None