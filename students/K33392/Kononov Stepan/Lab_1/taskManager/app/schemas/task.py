from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .project import Project
    from .priority import Priority
    from .category import Category


class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    deadline: datetime
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    user_id: int
    project_id: int
    priority_id: int


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: datetime
    owner: 'User'
    project: 'Project'
    priority: 'Priority'
    categories: List['Category']

    class Config:
        from_attributes = True
