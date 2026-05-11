from datetime import datetime

from sqlmodel import SQLModel


class NotificationCreate(SQLModel):
    task_id: int | None = None
    message: str
    trigger_at: datetime
    is_read: bool = False


class NotificationUpdate(SQLModel):
    message: str | None = None
    trigger_at: datetime | None = None
    is_read: bool | None = None


class NotificationRead(SQLModel):
    id: int
    user_id: int
    task_id: int | None = None
    message: str
    trigger_at: datetime
    is_read: bool
    created_at: datetime
