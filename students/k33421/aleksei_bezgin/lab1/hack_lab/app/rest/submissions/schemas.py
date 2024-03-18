import datetime

from sqlmodel import SQLModel


class Team(SQLModel):
    id: int
    name: str


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


class Submission(SQLModel):
    id: int
    submission_data: str
    evaluation: int | None = None

    team: Team
    task: Task


class SubmissionCreateData(SQLModel):
    submission_data: str
    evaluation: int | None = None
    team_id: int
    task_id: int


class SubmissionUpdateData(SQLModel):
    submission_data: str | None = None
    evaluation: int | None = None
    team_id: int | None = None
    task_id: int | None = None