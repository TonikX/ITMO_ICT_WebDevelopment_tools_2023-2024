from datetime import date

from pydantic import BaseModel
from typing import Optional, List

# Схема данных для создания пользователя
class UserCreate(BaseModel):
    username: str
    hashed_password: str
    is_active: Optional[bool] = True

# Схема данных для чтения пользователя
class UserRead(BaseModel):
    id: int
    username: str
    is_active: bool

# Схема данных для обновления пользователя
class UserUpdate(BaseModel):
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None

class UserList(BaseModel):
    users: List[UserRead]

class TaskBase(BaseModel):
    title: str
    description: str
    deadline: date
    priority: int
    user_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    priority: Optional[int] = None

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

class TaskList(BaseModel):
    tasks: List[Task]


