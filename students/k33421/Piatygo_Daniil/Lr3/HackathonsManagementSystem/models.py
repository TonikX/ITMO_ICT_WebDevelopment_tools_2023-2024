from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from schemas import TeamBase, ParticipantBase, HackathonBase, TaskBase, SubmissionBase, UserBase


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hackathons: List["TeamHackathon"] = Relationship(back_populates="team")
    participants: List["Participant"] = Relationship(back_populates="team")
    submissions: List["Submission"] = Relationship(back_populates="team")


class Participant(ParticipantBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: Optional[int] = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="participants")


class Hackathon(HackathonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: List["TeamHackathon"] = Relationship(back_populates="hackathon")
    tasks: List["Task"] = Relationship(back_populates="hackathon")


class TeamHackathon(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    hackathon_id: int = Field(foreign_key="hackathon.id", primary_key=True)
    registration_date: datetime
    team: Team = Relationship(back_populates="hackathons")
    hackathon: Hackathon = Relationship(back_populates="teams")


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hackathon_id: int = Field(foreign_key="hackathon.id")
    hackathon: Hackathon = Relationship(back_populates="tasks")
    submissions: List["Submission"] = Relationship(back_populates="task")


class Submission(SubmissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="submissions")
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="submissions")


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


Team.update_forward_refs()
Participant.update_forward_refs()
Hackathon.update_forward_refs()
TeamHackathon.update_forward_refs()
Task.update_forward_refs()
Submission.update_forward_refs()
