from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    name: str


class Contest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    start_time: datetime
    end_time: datetime


class Participant(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    contest_id: int = Field(default=None, foreign_key="contest.id")
    name: str
    email: str
    phone: str


class GetParticipant(SQLModel):
    id: int
    user_id: int
    contest_id: int
    name: str
    email: str
    phone: str
    is_approval: bool = False


class ParticipantApprovals(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    participant_id: int = Field(default=None, foreign_key="participant.id")


class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    contest_id: int = Field(default=None, foreign_key="contest.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str
    description: str
    requirements: str
    criteria: str


class Work(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: int = Field(default=None, foreign_key="task.id")
    user_id: int = Field(default=None, foreign_key="user.id")
    description: str


class Team(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str


class TeamMember(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    team_id: int = Field(default=None, foreign_key="team.id")


class UserRegistration(SQLModel):
    username: str
    password: str
    name: str
    email: str


class UserLogin(SQLModel):
    username: str
    password: str


class CreateContest(SQLModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime


class EditContest(SQLModel):
    id: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime


class CreateParticipant(SQLModel):
    contest_id: int = Field(default=None, foreign_key="contest.id")
    name: str
    email: str
    phone: str


class EditParticipant(SQLModel):
    id: int
    name: str
    email: str
    phone: str


class CreateTask(SQLModel):
    contest_id: int = Field(default=None, foreign_key="contest.id")
    name: str
    description: str
    requirements: str
    criteria: str


class EditTask(SQLModel):
    id: int
    name: str
    description: str
    requirements: str
    criteria: str


class CreateWork(SQLModel):
    task_id: int = Field(default=None, foreign_key="task.id")
    description: str


class EditWork(SQLModel):
    id: int
    description: str


class CreateParticipantApproval(SQLModel):
    participant_id: int = Field(default=None, foreign_key="participant.id")


class DeleteParticipantApproval(SQLModel):
    participant_id: int = Field(default=None, foreign_key="participant.id")


class CreateTeam(SQLModel):
    name: str


class EditTeam(SQLModel):
    id: int
    name: str


class CreateTeamMember(SQLModel):
    team_id: int = Field(default=None, foreign_key="team.id")


class DeleteTeamMember(SQLModel):
    team_id: int = Field(default=None, foreign_key="team.id")


class EditUser(SQLModel):
    name: str


class GetUser(BaseModel):
    id: int
    username: str
    name: str
    teams: List[Team] = []
    members: List[TeamMember] = []
    participants: List[GetParticipant] = []

class WorkGrade(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    work_id: int = Field(default=None, foreign_key="work.id")
    grade: int
    description: str

class CreateWorkGrade(SQLModel):
    work_id: int
    grade: int
    description: str

class EditWorkGrade(SQLModel):
    id: int
    grade: int
    description: str