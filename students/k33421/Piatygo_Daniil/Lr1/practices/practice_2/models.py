from datetime import datetime
from enum import Enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class ApproveStatus(str, Enum):
    gathering = "Gathering"
    completed = "Completed"
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


class SubmissionStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


class Skill(str, Enum):
    programming = "Programming"
    design = "Design"
    data_analysis = "Data Analysis"
    marketing = "Marketing"
    management = "Management"
    other = "Other"


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    approve_status: ApproveStatus
    hackathons: List["TeamHackathon"] = Relationship(back_populates="team")
    participants: List["Participant"] = Relationship(back_populates="team")
    submissions: List["Submission"] = Relationship(back_populates="team")


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    nickname: str
    email: str
    phone: str
    skill: Skill
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="participants")


class Hackathon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    teams: List["TeamHackathon"] = Relationship(back_populates="hackathon")
    tasks: List["Task"] = Relationship(back_populates="hackathon")
    submissions: List["Submission"] = Relationship(back_populates="hackathon")


class TeamHackathon(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    hackathon_id: int = Field(foreign_key="hackathon.id", primary_key=True)
    registration_date: datetime
    team: Team = Relationship(back_populates="hackathons")
    hackathon: Hackathon = Relationship(back_populates="teams")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    requirements: str
    evaluation_criteria: str
    hackathon_id: int = Field(foreign_key="hackathon.id")
    hackathon: Hackathon = Relationship(back_populates="tasks")
    submissions: List["Submission"] = Relationship(back_populates="task")


class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: Optional[str]
    file_url: Optional[str]
    status: SubmissionStatus
    task_id: int = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="submissions")
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="submissions")
    hackathon_id: int = Field(foreign_key="hackathon.id")
    hackathon: Hackathon = Relationship(back_populates="submissions")


Team.update_forward_refs()
Participant.update_forward_refs()
Hackathon.update_forward_refs()
TeamHackathon.update_forward_refs()
Task.update_forward_refs()
Submission.update_forward_refs()
