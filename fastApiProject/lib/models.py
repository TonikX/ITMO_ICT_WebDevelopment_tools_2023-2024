from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON


class SkillEnum(str, Enum):
    frontend = "Frontend"
    backend = "Backend"
    fullstack = "Fullstack"
    devops = "DevOps"
    mobile = "Mobile"
    data_science = "Data Science"


class UserTeam(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    position: str


class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional["User"] = Relationship(back_populates="profile")
    avatar: Optional[str] = None
    birth_date: Optional[str] = None
    skills: List[SkillEnum] = Field(sa_type=JSON)


class UserDefault(SQLModel):
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)


class User(UserDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: List["Team"] = Relationship(back_populates="users", link_model=UserTeam)
    profile_id: Optional[int] = Field(foreign_key="userprofile.id")
    profile: UserProfile = Relationship(back_populates="user")


class UserWithProfile(UserDefault):
    profile: Optional[UserProfile] = None


class TeamDefault(SQLModel):
    name: str


class Team(TeamDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List[User] = Relationship(back_populates="teams", link_model=UserTeam)
    projects: List["Project"] = Relationship(back_populates="team")


class TeamWithUsers(TeamDefault):
    users: List[UserWithProfile] = []


class ProjectDefault(SQLModel):
    name: str
    description: Optional[str]
    expected_result: Optional[str]


class Project(ProjectDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="projects")
    tasks: List["Task"] = Relationship(back_populates="project")


class ProjectWithTasksAndTeam(ProjectDefault):
    tasks: List["Task"] = []
    team: Optional[Team] = None


class TaskDefault(SQLModel):
    name: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None


class Task(TaskDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    project: Optional[Project] = Relationship(back_populates="tasks")
