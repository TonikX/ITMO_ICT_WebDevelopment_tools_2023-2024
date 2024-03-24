from enum import Enum
from typing import Optional, List

# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class Genre(str, Enum):
    Fiction = "fiction"
    NonFiction = "non-fiction"
    Mystery = "mystery"
    Romance = "romance"
    ScienceFiction = "science-fiction"


class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    bio: Optional[str] = ""

    books: List["Book"] = Relationship(back_populates="author")


class ExchangeRequestLink(SQLModel, table=True):
    __tablename__ = "exchange_request_link"

    exchange_request_id: int = Field(default=None, foreign_key="exchange_request.id", primary_key=True)
    user_id: int = Field(default=None, foreign_key="user_profile.id", primary_key=True)
    book_id: int = Field(default=None, foreign_key="book.id", primary_key=True)


class ExchangeRequest(SQLModel, table=True):
    __tablename__ = "exchange_request"

    id: int = Field(primary_key=True)
    books_offered: List["Book"] = Relationship(
        back_populates="exchange_requests_offered",
        link_model=ExchangeRequestLink
    )
    books_requested: List["Book"] = Relationship(
        back_populates="exchange_requests_requested",
        link_model=ExchangeRequestLink
    )
    accepted: bool
    users: List["UserProfile"] = Relationship(
        back_populates="exchange_requests",
        link_model=ExchangeRequestLink
    )


class UserDefault(SQLModel):
    username: str
    firstname: Optional[str]
    lastname: Optional[str]
    age: int
    location: Optional[str]
    bio: Optional[str]


class UserProfile(UserDefault, table=True):
    __tablename__ = "user_profile"

    id: int = Field(default=None, primary_key=True)
    exchange_requests: List["ExchangeRequest"] = Relationship(
        back_populates="users",
        link_model=ExchangeRequestLink
    )
    library: Optional["UserLibrary"] = Relationship(back_populates="user_profile")


class BookDefault(SQLModel):
    title: str
    author_id: int = Field(foreign_key="author.id")
    genre: Genre
    bio: Optional[str] = ""


class UserLibrary(SQLModel, table=True):
    __tablename__ = "user_library"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user_profile.id")
    book_id: int = Field(foreign_key="book.id")
    user_profile: UserProfile = Relationship(back_populates="library")
    books: Optional[List["Book"]] = Relationship(back_populates="user_library")


class Book(BookDefault, table=True):
    __tablename__ = "book"

    id: int = Field(default=None, primary_key=True)
    exchange_requests_offered: List["ExchangeRequest"] = Relationship(
        back_populates="books_offered",
        link_model=ExchangeRequestLink
    )
    exchange_requests_requested: List["ExchangeRequest"] = Relationship(
        back_populates="books_requested",
        link_model=ExchangeRequestLink
    )
    # user_library_id: int = Field(default=None, foreign_key="user_library.id")
    user_library: UserLibrary = Relationship(back_populates="books")
    author: Optional[Author] = Relationship(back_populates="books")


class BooksAuthor(BookDefault):
    author: Optional[Author] = None
