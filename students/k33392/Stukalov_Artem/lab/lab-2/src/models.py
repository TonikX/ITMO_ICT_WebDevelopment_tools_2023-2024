from sqlmodel import SQLModel, Field, Relationship  # type: ignore
from typing import List, Optional
from enum import Enum
from datetime import datetime

# Link models


class BookOwnership(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")


class WishlistItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")


# ExchangeRequest
class ExchangeRequestStatus(Enum):
    pending = "pending"
    confirmed = "confirmed"
    declined = "declined"


class ExchangeRequestGet(SQLModel):
    status: ExchangeRequestStatus
    received: bool
    sent: bool
    created_at: datetime


class ExchangeRequestGetWithRelations(SQLModel):
    sender: "User"
    receiver: "User"
    book_ownership: BookOwnership


class ExchangeRequestUpdateStatus(SQLModel):
    status: Optional[ExchangeRequestStatus] = None
    received: Optional[bool] = None
    sent: Optional[bool] = None


class ExchangeRequestCreate(SQLModel):
    book_ownership_id: int
    receiver_id: int


class ExchangeRequestBase(SQLModel):
    status: ExchangeRequestStatus = Field(default=ExchangeRequestStatus.pending)
    received: bool = Field(default=False)
    sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)


class ExchangeRequest(ExchangeRequestBase, table=True):
    id: int = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(foreign_key="user.id")
    book_ownership_id: int = Field(foreign_key="bookownership.id")

    sender: "User" = Relationship(
        back_populates="sent_exchange_requests",
        sa_relationship_kwargs=dict(foreign_keys="[ExchangeRequest.sender_id]"),
    )
    receiver: "User" = Relationship(
        back_populates="received_exchange_requests",
        sa_relationship_kwargs=dict(foreign_keys="[ExchangeRequest.receiver_id]"),
    )
    book_ownership: BookOwnership = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[ExchangeRequest.book_ownership_id]"),
    )


# User
class UserGet(SQLModel):
    username: str
    bio: Optional[str]
    is_admin: bool


class UserGetWithRelations(UserGet):
    books: List["Book"] = []
    sent_exchange_requests: List["ExchangeRequest"] = []
    received_exchange_requests: List["ExchangeRequest"] = []
    wishlist: List["Book"] = []


class UserCreate(SQLModel):
    username: str
    password: str
    bio: Optional[str] = None


class WishlistAdd(SQLModel):
    book_id: int


class WishlistRemove(WishlistAdd):
    pass


class Token(SQLModel):
    access_token: str
    token_type: str


class UserBase(SQLModel):
    username: str = Field(unique=True)
    pass_hash: str
    bio: Optional[str] = Field(default=None)
    is_admin: bool = Field(default=False)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(
        back_populates="owners", link_model=BookOwnership
    )
    sent_exchange_requests: List["ExchangeRequest"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs=dict(foreign_keys="[ExchangeRequest.sender_id]"),
    )
    received_exchange_requests: List["ExchangeRequest"] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs=dict(foreign_keys="[ExchangeRequest.receiver_id]"),
    )
    wishlist: List["Book"] = Relationship(link_model=WishlistItem)


# Book
class BookModerationStatus(Enum):
    pending = "pending"
    approved = "approved"


class BookBase(SQLModel):
    title: str = Field(unique=True)
    author: str
    year: Optional[int] = Field(default=None)
    creator_id: int = Field(foreign_key="user.id")
    moderation_status: BookModerationStatus = Field(
        default=BookModerationStatus.pending
    )


class Book(BookBase, table=True):
    id: int = Field(default=None, primary_key=True)
    owners: List["User"] = Relationship(
        back_populates="books", link_model=BookOwnership
    )


class BookCreate(SQLModel):
    title: str
    author: str
    year: Optional[int]


class BookGet(BookBase):
    pass


class BookGetWithRelations(BookGet):
    owners: List["User"] = []


class BookUpdateStatus(SQLModel):
    moderation_status: BookModerationStatus


class BookCreateOwned(SQLModel):
    book_id: int
