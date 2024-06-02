from enum import Enum
from typing import Optional, List, Union
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class BookGenres(str, Enum):
    Fiction = "fiction"
    NonFiction = "non-fiction"
    Mystery = "mystery"
    Romance = "romance"
    ScienceFiction = "science-fiction"


class AuthorBookLink(SQLModel, table=True):
    __tablename__ = "author_book_link"

    author_id: int = Field(default=None, foreign_key="author.id", primary_key=True)
    book_id: int = Field(default=None, foreign_key="book.id", primary_key=True)


class AuthorDefault(SQLModel):
    name: str
    bio: Optional[str]
    country: Optional[str] = ""


class Author(AuthorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="authors", link_model=AuthorBookLink)


# class ExchangeRequestLink(SQLModel, table=True):
#     __tablename__ = "exchange_request_link"
#
#     exchange_request_id: int = Field(default=None, foreign_key="exchange_request.id", primary_key=True)
#     sender_id: int = Field(default=None, foreign_key="user_profile.id", primary_key=True)
#     receiver_id: int = Field(default=None, foreign_key="user_profile.id", primary_key=True)
#     offered_book_id: int = Field(default=None, foreign_key="book.id", primary_key=True)
#     requested_book_id: int = Field(default=None, foreign_key="book.id", primary_key=True)


class ExchangeRequest(SQLModel, table=True):
    __tablename__ = "exchange_request"

    id: int = Field(primary_key=True)
    accepted: bool
    sender_id: int = Field(default=None, foreign_key="user_profile.id")
    receiver_id: int = Field(default=None, foreign_key="user_profile.id")

    sender: Optional["UserProfile"] = Relationship(
        back_populates="sent_requests",
        sa_relationship_kwargs={"foreign_keys": "ExchangeRequest.sender_id"}
    )
    receiver: Optional["UserProfile"] = Relationship(
        back_populates="received_requests",
        sa_relationship_kwargs={"foreign_keys": "ExchangeRequest.receiver_id"}
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
    # exchange_requests: List["ExchangeRequest"] = Relationship(
    #     back_populates="users",
    #     link_model=ExchangeRequestLink
    # )
    password_hash: str = Field(default=None)
    sent_requests: Optional[List["ExchangeRequest"]] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "ExchangeRequest.sender_id"}
    )
    received_requests: Optional[List["ExchangeRequest"]] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={"foreign_keys": "ExchangeRequest.receiver_id"}
    )
    # library: Optional["UserLibrary"] = Relationship(back_populates="user_profile")


class BookDefault(SQLModel):
    title: str
    # author_id: int = Field(foreign_key="author.id")
    genre: Optional[BookGenres]
    bio: Optional[str] = ""


class UserLibrary(SQLModel, table=True):
    __tablename__ = "user_library"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user_profile.id")
    book_id: int = Field(foreign_key="book.id")
    # user_profile: UserProfile = Relationship(back_populates="library")
    books_library: Optional[List["Book"]] = Relationship(back_populates="user_library")


class Book(BookDefault, table=True):
    __tablename__ = "book"

    id: int = Field(default=None, primary_key=True)
    # user_library_id: int = Field(default=None, foreign_key="user_library.id")
    user_library: UserLibrary = Relationship(back_populates="books_library")
    authors: Optional[List["Author"]] = Relationship(back_populates="books", link_model=AuthorBookLink)


class BooksAuthor(BookDefault):
    author: Optional[Author] = None


class BookWithAuthors(SQLModel):
    book: BookDefault
    author_ids: List[int]


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Union[str, None] = None
