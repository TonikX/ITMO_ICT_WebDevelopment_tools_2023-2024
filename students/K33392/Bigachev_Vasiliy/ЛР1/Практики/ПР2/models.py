from enum import Enum
from typing import Optional, List
from datetime import date, datetime

#from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

# Приоритет
class PriorityDefault(SQLModel):
    name: str

class Priority(PriorityDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks_priority: Optional[List["Task"]] = Relationship(back_populates="priority")
# Приоритет

# Тэг
class TagTaskLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)

class TagDefault(SQLModel):
    name: str

class Tag(TagDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="tags", link_model=TagTaskLink)
# Тэг

# Задача
class TaskDefault(SQLModel):
    title: str
    description: str
    dueTo: date
    priority_id: Optional[int] = Field(default=None, foreign_key="priority.id")

class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    priority: Optional[Priority] = Relationship(back_populates="tasks_priority")
    tags: Optional[List[Tag]] = Relationship(back_populates="tasks", link_model=TagTaskLink)

class TaskOut(TaskDefault):
    id: int
    priority: Optional[Priority] = None
    tags: Optional[List[Tag]] = None
# Задача