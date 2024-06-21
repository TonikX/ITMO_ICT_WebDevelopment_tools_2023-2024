import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Status(Enum):
    to_do = "Not started"
    in_progress = "In progress"
    review = "Waiting for review"
    testing = "Testing"
    finished = "Done"
    cancelled = "Cancelled"


class SkillUserLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    level: Optional[int] = None


class TeamSkillLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    required_level: Optional[int] = None


class SkillDefault(SQLModel):
    name: str
    description: Optional[str] = None


class Skill(SkillDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    users: Optional[List["User"]] = Relationship(back_populates="skills", link_model=SkillUserLink)


class SkillExtended(SkillDefault):
    id: int = None
    users: Optional[List["User"]] = None


class TeamUserLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    position: Optional[str] = None
    date_joined: datetime.date = Field(default_factory=datetime.date.today)
    exit_date: Optional[datetime.date] = None


class TeamUserLinkPartialUpdate(SQLModel):
    position: Optional[str] = None


class UserDefault(SQLModel):
    name: str
    about: Optional[str] = None
    experience: Optional[str] = None
    preferences: Optional[str] = None
    email: str = Field(unique=True)
    password: str
    contacts: Optional[str] = None


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    skills: Optional[List[Skill]] = Relationship(back_populates="users", link_model=SkillUserLink)
    tasks: Optional[List["Task"]] = Relationship(back_populates="responsible_user")
    teams: Optional[List["Team"]] = Relationship(back_populates="users", link_model=TeamUserLink)
    user_projects: Optional[List["UserProject"]] = Relationship(back_populates="user")


class UserAuth(SQLModel):
    email: str = None
    password: str = None


class UserExtended(SQLModel):
    id: int = None
    skills: Optional[List[Skill]] = None
    tasks: Optional[List["Task"]] = None
    teams: Optional[List["Team"]] = None
    user_projects: Optional[List["UserProject"]] = None
    name: str
    about: Optional[str] = None
    experience: Optional[str] = None
    preferences: Optional[str] = None
    email: str
    contacts: Optional[str] = None


class UserPartialUpdate(SQLModel):
    name: Optional[str] = None
    about: Optional[str] = None
    experience: Optional[str] = None
    preferences: Optional[str] = None
    email: Optional[str] = None
    contacts: Optional[str] = None


class TeamDefault(SQLModel):
    name: str
    description: Optional[str] = None
    date_created: datetime.date = Field(default_factory=datetime.date.today)


class Team(TeamDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    users: List[User] = Relationship(back_populates="teams", link_model=TeamUserLink)
    team_projects: Optional[List["TeamProject"]] = Relationship(back_populates="team")


class TeamExtended(TeamDefault):
    id: int = None
    users: List[User] = None
    team_projects: Optional[List["TeamProject"]] = None


class TeamPartialUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TeamProjectDefault(SQLModel):
    team_id: int = Field(default=None, foreign_key="team.id")
    name: str
    description: Optional[str] = None
    status: Status
    date_started: datetime.date = Field(default_factory=datetime.date.today)
    date_finished: Optional[datetime.date] = None
    progress: Optional[int] = None


class TeamProject(TeamProjectDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    team: Team = Relationship(back_populates="team_projects")
    tasks: Optional[List["Task"]] = Relationship(back_populates="team_project")


class TeamProjectExtended(TeamProjectDefault):
    id: int = None
    team: Team = None
    tasks: Optional[List["Task"]] = None


class TeamProjectPartialUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    date_finished: Optional[datetime.date] = None
    progress: Optional[int] = None


class UserProjectDefault(SQLModel):
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str
    description: Optional[str] = None
    status: Optional[Status] = None
    in_search: bool
    people_required: Optional[str] = None


class UserProjectPartialUpdate(SQLModel):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    in_search: Optional[bool] = None
    people_required: Optional[str] = None


class UserProject(UserProjectDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="user_projects")


class UserProjectExtended(UserProjectDefault):
    id: int = None
    user: User = None


class TaskDefault(SQLModel):
    responsible_user_id: int = Field(default=None, foreign_key="user.id")
    team_project_id: int = Field(default=None, foreign_key="teamproject.id")
    name: str
    description: Optional[str] = None
    status: Status
    deadline: Optional[datetime.date] = None
    date_started: Optional[datetime.date] = None
    date_finished: Optional[datetime.date] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    responsible_user: User = Relationship(back_populates="tasks")
    team_project: TeamProject = Relationship(back_populates="tasks")


class TaskExtended(TaskDefault):
    responsible_user: User = None
    team_project: TeamProject = None


class TaskPartialUpdate(SQLModel):
    responsible_user_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    deadline: Optional[datetime.date] = None
    date_started: Optional[datetime.date] = None
    date_finished: Optional[datetime.date] = None
