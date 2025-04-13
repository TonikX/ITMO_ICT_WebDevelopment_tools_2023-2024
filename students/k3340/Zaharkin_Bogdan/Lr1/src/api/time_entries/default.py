from sqlmodel import SQLModel, Field
from datetime import datetime


# TimeEntry table
class TimeEntryDefault(SQLModel):
    task_id: int | None = Field(default=None, foreign_key="task.id")
    start_time: datetime
    end_time: datetime
    duration: int
