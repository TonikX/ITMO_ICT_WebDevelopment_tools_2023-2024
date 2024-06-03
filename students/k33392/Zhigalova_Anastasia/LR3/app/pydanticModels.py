from pydantic import BaseModel
from models import *


class UserUpdate(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class TimeLogCreate(BaseModel):
    task_id: int
    time_spent_minutes: int
    date_logged: date

class TaskCategoryCreate(BaseModel):
    task_id: int
    category_id: int
    additional_info: str

class TaskCategoryUpdate(BaseModel):
    task_id: int
    category_id: int
    additional_info: str

    class Config:
        orm_mode = True


class TaskName(BaseModel):
    title: str

class UserWithTaskNames(BaseModel):
    id: int
    username: str
    tasks: List[TaskName]


class UserInDB(UserCreate):
    hashed_password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class PasswordChange(BaseModel):
    old_password: str
    new_password: str