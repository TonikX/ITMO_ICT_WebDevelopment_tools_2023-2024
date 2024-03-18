import datetime

from sqlmodel import SQLModel


class Team(SQLModel):
    id: int
    name: str


class Submission(SQLModel):
    id: int
    submission_data: str
    evaluation: int | None = None

    team: Team


class Hackathon(SQLModel):
    id: int
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class Task(SQLModel):
    id: int
    title: str
    description: str
    requirements: str
    evaluation_criteria: str

    hackathon: Hackathon
    submissions: list[Submission]


class TaskCreateData(SQLModel):
    title: str
    description: str
    requirements: str
    evaluation_criteria: str
    hackathon_id: int


class TaskUpdateData(SQLModel):
    title: str | None = None
    description: str | None = None
    requirements: str | None = None
    evaluation_criteria: str | None = None
    hackathon_id: int | None = None