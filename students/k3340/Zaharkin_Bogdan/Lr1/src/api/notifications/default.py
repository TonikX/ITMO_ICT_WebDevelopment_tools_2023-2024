from sqlmodel import SQLModel, Field
from datetime import datetime


# Notification table
class NotificationDefault(SQLModel):
    task_id: int | None = Field(default=None, foreign_key="task.id")
    message: str
    sent_at: datetime
