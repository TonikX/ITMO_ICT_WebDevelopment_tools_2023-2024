"""Pydantic-схемы (валидация запросов и сериализация ответов)."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import HackathonStatus, UserRole


# --------------------------- Пользователи / Auth ---------------------------

class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    password: str = Field(..., min_length=6, max_length=128)
    role: UserRole = UserRole.participant


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str]
    role: UserRole
    is_confirmed: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=128)


class MessageOut(BaseModel):
    detail: str


# ------------------------------- Хакатоны ----------------------------------

class HackathonCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: HackathonStatus = HackathonStatus.planned


class HackathonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    location: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: HackathonStatus
    created_at: datetime


# -------------------------------- Команды ----------------------------------

class TeamCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = None
    hackathon_id: int
    # Роль создателя в команде (характеризующее поле связи).
    role_in_team: str = Field("captain", max_length=80)


class TeamJoin(BaseModel):
    role_in_team: str = Field("member", max_length=80)


class TeamMemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    team_id: int
    role_in_team: str
    joined_at: datetime
    user: UserOut


class TeamOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    hackathon_id: int
    created_at: datetime


class TeamDetailOut(TeamOut):
    members: List[TeamMemberOut] = []


# --------------------------------- Задачи ----------------------------------

class TaskCreate(BaseModel):
    hackathon_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    requirements: Optional[str] = None
    evaluation_criteria: Optional[str] = None
    max_score: float = 100.0


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hackathon_id: int
    title: str
    description: Optional[str]
    requirements: Optional[str]
    evaluation_criteria: Optional[str]
    max_score: float
    created_at: datetime


# -------------------------- Работы / Оценки --------------------------------

class SubmissionCreate(BaseModel):
    team_id: int
    task_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    repo_url: Optional[str] = Field(None, max_length=300)


class EvaluationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    submission_id: int
    judge_id: int
    score: float
    comment: Optional[str]
    created_at: datetime


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    team_id: int
    task_id: int
    title: str
    description: Optional[str]
    repo_url: Optional[str]
    submitted_at: datetime


class SubmissionDetailOut(SubmissionOut):
    evaluations: List[EvaluationOut] = []


class EvaluationCreate(BaseModel):
    score: float = Field(..., ge=0)
    comment: Optional[str] = None
