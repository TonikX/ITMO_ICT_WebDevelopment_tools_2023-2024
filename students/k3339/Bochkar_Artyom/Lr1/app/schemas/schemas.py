from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import validator, EmailStr


# Enum для поля пола
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


# Enum для статуса заявки
class RequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


# Схемы для создания
class ProfileCreate(SQLModel):
    username: str
    name: str
    surname: str
    age: int
    gender: Gender
    address: Optional[str] = None
    email: EmailStr
    password: str
    confirm_password: str


class ProfileUpdate(SQLModel):
  username: Optional[str] = None
  name: Optional[str] = None
  surname: Optional[str] = None
  age: Optional[int] = None
  gender: Optional[Gender] = None
  address: Optional[str] = None


class BookCreate(SQLModel):
    title: str
    author: str
    genre: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


class BookUpdate(SQLModel):
  title: Optional[str] = None
  author: Optional[str] = None
  genre: Optional[str] = None
  description: Optional[str] = None
  pages: Optional[int] = None
  owner_id: Optional[int] = None


class ExchangeRequestCreate(SQLModel):
    book_id: int
    requester_id: int

class ExchangeRequestUpdate(SQLModel):
    status: RequestStatus


# Схемы для ответов
class BookRead(SQLModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileRead(SQLModel):
    id: int
    username: str
    name: str
    surname: str
    age: int
    gender: Gender
    address: Optional[str] = None
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True


class ExchangeRequestRead(SQLModel):
    id: int
    book_id: int
    requester_id: int
    status: RequestStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ExchangeRequestWithDetails(SQLModel):
    id: int
    status: RequestStatus
    created_at: datetime
    book: BookRead
    requester: ProfileRead

    class Config:
        from_attributes = True


class ProfileWithBooks(ProfileRead):
    books: List[BookRead] = []


class ProfileWithRequests(ProfileRead):
    sent_requests: List[ExchangeRequestRead] = []
    received_requests: List[ExchangeRequestRead] = []


class BookWithRequests(BookRead):
    requests: List[ExchangeRequestRead] = []


class UserRegisterWithProfile(SQLModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    name: str
    surname: str
    age: int
    gender: Gender
    address: Optional[str] = None
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def password_length(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    

class UserRegisterResponse(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        from_attributes = True


class UserLogin(SQLModel):
    username: str
    password: str

class TokenLogin(SQLModel):
    token: str


class UserCreate(SQLModel):
    username: str
    email: EmailStr
    hashed_password: str
    salt: str

# Схемы для ответов
class UserRead(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(SQLModel):
    username: Optional[str] = None

class LoginResponse(SQLModel):
    user: UserRead
