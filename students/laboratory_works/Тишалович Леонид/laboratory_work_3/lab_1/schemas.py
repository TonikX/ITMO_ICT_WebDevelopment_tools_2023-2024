import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Urgency(Enum):
    emergency = 'emergency'
    urgently = 'urgently'
    no_hurry = 'no_hurry'
    one_day = 'one_day'


class TeamMemberDefault(SQLModel):
    participant_id:  Optional[int] = Field(default=None, foreign_key="participant.id")
    team_id:  Optional[int] = Field(default=None, foreign_key="team.id")


class TeamMember(TeamMemberDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    participants: Optional["Participant"] = Relationship(back_populates="teammembers")
    teams: Optional["Team"] = Relationship(back_populates="teammembers")


class SubmissionDefault(SQLModel):
    task_id:  Optional[int] = Field(default=None, foreign_key="task.id")
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    work_link: str
    urgency: Urgency

class Submission(SubmissionDefault, table=True):

    id: int = Field(default=None, primary_key=True)

    tasks: Optional["Task"] = Relationship(back_populates="submissions")
    teams: Optional["Team"] = Relationship(back_populates="submissions")



class ParticipantDefault(SQLModel):
    username: str
    email: str
    password: str
    contact_number: str


class Participant(ParticipantDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    teams: Optional[List["Team"]] = Relationship(
        back_populates="participants", link_model=TeamMember
    )
    teammembers: Optional[List["TeamMember"]] = Relationship(back_populates="participants")



class TeamDefault(SQLModel):
    name: str
    description: str

class Team(TeamDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    participants: Optional[List["Participant"]] = Relationship(
        back_populates="teams", link_model=TeamMember
    )
    teammembers: Optional[List["TeamMember"]] = Relationship(back_populates="teams")

    tasks: Optional[List["Task"]] = Relationship(
        back_populates="teams", link_model=Submission
    )
    submissions: Optional[List["Submission"]] = Relationship(back_populates="teams")

class TaskDefault(SQLModel):
    title: str
    description: str
    requirements: str
    evaluation_criteria: str

class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    teams: Optional[List["Team"]] = Relationship(
        back_populates="tasks", link_model=Submission
    )
    submissions: Optional[List["Submission"]] = Relationship(back_populates="tasks")



class ParticipantDisplay(ParticipantDefault):
    teams: Optional[List["Team"]] = None
    teammembers: Optional[List["TeamMember"]] = None

class TeamDisplay(TeamDefault):
    participants: Optional[List["Participant"]] = None
    teammembers: Optional[List["TeamMember"]] = None
    tasks: Optional[List["Task"]] = None
    submissions: Optional[List["Submission"]] = None

class TaskDisplay(TaskDefault):
    teams: Optional[List["Team"]] = None
    submissions: Optional[List["Submission"]] = None


class Login(SQLModel):
    username: str
    password: str
class ChangePassword(SQLModel):
    old_password: str
    new_password: str


class Site(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    title: str
