from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from typing import Optional, List
from enum import Enum
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StatusEnum(Enum):
    to_do = "To do"
    in_progress = "In progress"
    done = "Done"


class PriorityEnum(Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class LabelTaskLink(SQLModel, table=True):
    label_id: Optional[int] = Field(
        default=None, foreign_key="label.id", primary_key=True
    )
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    level: int | None


class LabelDefault(SQLModel):
    content: Optional[str] = ""
    created_at: date = Field(default_factory=date.today)


class Label(LabelDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="labels", link_model=LabelTaskLink)


class CategoryDefault(SQLModel):
    title: str
    description: Optional[str] = ""


class Category(CategoryDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task_cat: List["Task"] = Relationship(back_populates="category")


class UserDefault(SQLModel):
    username: str
    password: str
    email: str
    registration_date: date = Field(default_factory=date.today)


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = None
    task_user: List["Task"] = Relationship(back_populates="user")

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)


class TaskTime(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="task_time")


class TaskDefault(SQLModel):
    title: str
    description: str
    deadline: date
    created_date: date = Field(default_factory=date.today)
    priority: PriorityEnum
    status: StatusEnum
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    category: Optional[Category] = Relationship(back_populates="task_cat")
    user: Optional[User] = Relationship(back_populates="task_user")
    labels: Optional[List[Label]] = Relationship(back_populates="tasks", link_model=LabelTaskLink)
    task_time: Optional["TaskTime"] = Relationship(
        back_populates="task"
    )


class TasksDetails(TaskDefault):
    user: Optional[User] = None
    category: Optional[Category] = None
    task_time: Optional[TaskTime] = None
    labels: Optional[List[Label]] = None


class Token(SQLModel):
    access_token: str
    token_type: str
