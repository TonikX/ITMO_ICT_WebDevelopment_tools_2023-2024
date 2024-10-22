from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

#user-team link
class UserTeamLink(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)

#user
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    teams: Optional[List["Team"]] = Relationship(back_populates="members", link_model=UserTeamLink)
    
#team
class TeamDefault(SQLModel):
    name: str

class Team(TeamDefault, table=True):
    id: int = Field(primary_key=True)
    members: List["User"] = Relationship(back_populates="teams", link_model=UserTeamLink)
    projects: Optional[List["Project"]] = Relationship(back_populates="team")

class TeamResponse(TeamDefault):
    id: int
    members: List["User"] = []
    projects: List["Project"] = []

#competition
class CompetitionDefault(SQLModel):
    name: str
    description: str

class Competition(CompetitionDefault, table=True):
    id: int = Field(primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="comp")

class CompetitionResponse(CompetitionDefault):
    id: int
    tasks: List["Task"] = []

#task 
class TaskDefault(SQLModel):
    name: str
    description: str
    deadline: datetime
    comp_id: int = Field(foreign_key="competition.id")


class Task(TaskDefault, table=True):
    id: int = Field(primary_key=True)
    comp: Competition = Relationship(back_populates="tasks")
    solutions: Optional[List["Project"]] = Relationship(back_populates="task")


class TaskResponse(TaskDefault):
    id: int
    comp: Competition = None
    solutions: List["Project"] = []


# project
class ProjectNomination(Enum):
    first = "first"
    second = "second"
    third = "third"
    participant = "participant"


class ProjectDefault(SQLModel):
    name: str
    description: str
    grade: Optional[int]
    nomination: ProjectNomination
    task_id: int = Field(foreign_key="task.id")
    team_id: int = Field(foreign_key="team.id")


class Project(ProjectDefault, table=True):
    id: int = Field(primary_key=True)
    task: Task = Relationship(back_populates="solutions")
    team: Team = Relationship(back_populates="projects")


class ProjectResponse(ProjectDefault):
    id: int
    task: Task = None
    team: Team = None