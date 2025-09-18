from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enum для поля пола
class Gender(str, Enum):
  MALE = "male"
  FEMALE = "female"


# Enum для статуса заявки
class RequestStatus(str, Enum):
  PENDING = "pending"
  ACCEPTED = "accepted"
  REJECTED = "rejected"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    salt: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
  

# Базовые модели для валидации данных
class ProfileBase(SQLModel):
  username: str = Field(index=True, unique=True)
  name: str
  surname: str
  age: int
  gender: Gender
  address: Optional[str] = None


class BookBase(SQLModel):
  title: str
  author: str
  genre: Optional[str] = None
  description: Optional[str] = None
  pages: Optional[int] = None


class ExchangeRequestBase(SQLModel):
  status: RequestStatus = Field(default=RequestStatus.PENDING)


# Модели для базы данных
class Profile(ProfileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", unique=True)
    user: Optional[User] = Relationship()
    
    books: List["Book"] = Relationship(back_populates="owner")
    sent_requests: List["ExchangeRequest"] = Relationship(back_populates="requester")


class Book(BookBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  owner_id: Optional[int] = Field(default=None, foreign_key="profile.id")
  created_at: datetime = Field(default_factory=datetime.utcnow)

  owner: Optional[Profile] = Relationship(back_populates="books")
  requests: List["ExchangeRequest"] = Relationship(back_populates="book")


class ExchangeRequest(ExchangeRequestBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  book_id: int = Field(foreign_key="book.id")
  requester_id: int = Field(foreign_key="profile.id")
  created_at: datetime = Field(default_factory=datetime.utcnow)

  book: "Book" = Relationship(back_populates="requests")
  requester: "Profile" = Relationship(back_populates="sent_requests")
