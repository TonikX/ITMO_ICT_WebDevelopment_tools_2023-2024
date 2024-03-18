from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel
from typing import List, Optional


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


class TeamBase(SQLModel):
    name: str
    approve_status: ApproveStatus


class ParticipantBase(SQLModel):
    full_name: str
    nickname: str
    email: str
    phone: str
    skill: Skill


class HackathonBase(SQLModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime


class TaskBase(SQLModel):
    title: str
    description: str
    requirements: str
    evaluation_criteria: str


class SubmissionBase(SQLModel):
    code: Optional[str]
    file_url: Optional[str]
    status: SubmissionStatus


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class ParticipantResponse(ParticipantBase):
    id: Optional[int]

    class Config:
        from_attributes = True


class TeamResponse(TeamBase):
    participants: List[ParticipantResponse] = []

    class Config:
        from_attributes = True


class TaskResponse(TaskBase):
    id: Optional[int]

    class Config:
        from_attributes = True


class HackathonResponse(HackathonBase):
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True


class UserResponse(SQLModel):
    id: Optional[int]
    username: str
    email: str

    class Config:
        from_attributes = True


class ChangePasswordBody(SQLModel):
    old_password: str
    new_password: str
