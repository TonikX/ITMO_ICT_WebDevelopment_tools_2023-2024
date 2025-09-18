from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
  MALE = "male"
  FEMALE = "female"

class ProfileBase(SQLModel):
  username: str = Field(index=True, unique=True)
  name: str
  surname: str
  age: int
  gender: Gender
  address: Optional[str] = None

class Profile(ProfileBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  created_at: datetime = Field(default_factory=datetime.utcnow)

  books: List["Book"] = Relationship(back_populates="owner")

class BookBase(SQLModel):
  title: str
  author: str
  genre: Optional[str] = None
  description: Optional[str] = None

class Book(BookBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  owner_id: Optional[int] = Field(default=None, foreign_key="profile.id")
  created_at: datetime = Field(default_factory=datetime.utcnow)

  owner: Optional[Profile] = Relationship(back_populates="books")