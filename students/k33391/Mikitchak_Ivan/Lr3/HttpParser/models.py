from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False, index=True)
    hashed_password: str
    last_logout: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    def __str__(self):
        return (f"User ("
                f"\"id\": {id}, "
                f"\"email\": {self.email}, "
                f"\"first_name\": {self.first_name}, "
                f"\"last_name\": {self.last_name})")


class UserSerialized(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
