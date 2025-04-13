from sqlmodel import SQLModel, Field
from datetime import datetime


# Schedule table
class ScheduleDefault(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    date: datetime
