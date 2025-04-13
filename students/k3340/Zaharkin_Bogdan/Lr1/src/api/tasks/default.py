from sqlmodel import SQLModel, Field
from datetime import datetime


# Task table
class TaskDefault(SQLModel):
    description: str
    deadline: datetime
    priority_id: int | None = Field(default=None, foreign_key="priority.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
