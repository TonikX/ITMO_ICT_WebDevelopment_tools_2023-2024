import typing as tp
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectJoin(BaseModel):
    role: str


class ProjectCRUD(BaseModel):
    title: str
    description: tp.Optional[str]
    is_active: bool
    start_date: datetime
    end_date: tp.Optional[datetime]


class Project(ProjectCRUD):
    id: int
    creator_id: tp.Optional[int]

    model_config = ConfigDict(from_attributes=True)
