from datetime import datetime

from sqlmodel import SQLModel


class UserRead(SQLModel):
    id: int
    email: str
    username: str
    created_at: datetime


class PasswordChangeRequest(SQLModel):
    old_password: str
    new_password: str
