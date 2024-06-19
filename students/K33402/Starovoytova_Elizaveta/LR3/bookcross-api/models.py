import datetime
from typing import Optional, List
from pydantic import validator, EmailStr
from sqlmodel import SQLModel, Field, Relationship, AutoString
from enum import Enum


class ExchangeStatus(Enum):
    agreed = "agreed"
    rejected = "rejected"
    notselected = "not selected"


# book instance
class BookInstanceBase(SQLModel):
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    date: datetime.datetime
    publisher: str
    features: str


class BookInstance(BookInstanceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    requests: Optional[List["BookExchange"]] = Relationship(
        back_populates="book_instance",
        sa_relationship_kwargs=dict(foreign_keys="[BookExchange.book_instance_id]"),
    )
    book: Optional["Book"] = Relationship(back_populates="instances")
    owner: Optional["User"] = Relationship(back_populates="instances")


class BookInstanceRead(BookInstanceBase):
    id: int
    owner_id: int


class BookInstanceWithBook(BookInstanceRead):
    book: "BookRead" = None


# author
class AuthorBase(SQLModel):
    name: str
    bio: str


class Author(AuthorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    books: Optional[List["Book"]] = Relationship(back_populates="author")


class AuthorRead(AuthorBase):
    id: int


# book
class BookBase(SQLModel):
    title: str
    description: str
    author_id: Optional[int] = Field(default=None, foreign_key="author.id")


class Book(BookBase, table=True):
    id: int = Field(default=None, primary_key=True)
    author: Optional[Author] = Relationship(back_populates="books")
    owners: Optional[List["User"]] = Relationship(back_populates="books", link_model=BookInstance)
    instances: Optional[List["BookInstance"]] = Relationship(back_populates="book")


class BookRead(BookBase):
    id: int


class AuthorReadFull(AuthorRead):
    books: list["BookRead"] = []


# user
class UserBase(SQLModel):
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    name: str
    about: str
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)


class BookReadFull(BookRead):
    author: AuthorRead = None
    owners: list["UserBase"] = []
    instances: list["BookInstanceRead"] = []


class User(UserBase, table=True):
    password: str = Field(max_length=256, min_length=6)
    created_at: datetime.datetime = datetime.datetime.now()
    books: Optional[List["Book"]] = Relationship(back_populates="owners", link_model=BookInstance)
    sender_requests: Optional[List["BookExchange"]] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs=dict(foreign_keys="[BookExchange.sender_id]"),
    )
    receiver_requests: Optional[List["BookExchange"]] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs=dict(foreign_keys="[BookExchange.receiver_id]"),
    )
    instances: Optional[List["BookInstance"]] = Relationship(back_populates="owner")


class UserInput(SQLModel):
    name: str
    about: str
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str
    password: str


class UserPassword(SQLModel):
    old_password: str
    new_password: str


# book exchange
class BookExchangeBase(SQLModel):
    book_instance_id: Optional[int] = Field(default=None, foreign_key="bookinstance.id")
    status: ExchangeStatus
    date_start: datetime.datetime
    date_end: datetime.datetime


class BookExchange(BookExchangeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sender_id: Optional[int] = Field(default=None, foreign_key="user.id")
    receiver_id: Optional[int] = Field(default=None, foreign_key="user.id")

    sender: Optional["User"] = Relationship(
        back_populates="sender_requests",
        sa_relationship_kwargs=dict(foreign_keys="[BookExchange.sender_id]"),
    )
    receiver: Optional["User"] = Relationship(
        back_populates="receiver_requests",
        sa_relationship_kwargs=dict(foreign_keys="[BookExchange.receiver_id]"),
    )
    book_instance: Optional["BookInstance"] = Relationship(
        back_populates="requests",
        sa_relationship_kwargs=dict(foreign_keys="[BookExchange.book_instance_id]"),
    )


class BookExchangeChangeStatus(SQLModel):
    status: ExchangeStatus


class BookExchangeRead(BookExchangeBase):
    id: int
    sender_id: int
    receiver_id: int


class UserReadFull(UserBase):
    sender_requests:  list["BookExchangeRead"] = []
    receiver_requests:  list["BookExchangeRead"] = []
    instances: list["BookInstanceWithBook"] = []


class BookInstanceReadFull(BookInstanceWithBook):
    requests: list["BookExchangeRead"] = []
    owner: "UserBase" = None


class BookExchangeReadFull(BookExchangeRead):
    sender: "UserBase" = None
    receiver: "UserBase" = None
    book_instance: "BookInstanceWithBook" = None
