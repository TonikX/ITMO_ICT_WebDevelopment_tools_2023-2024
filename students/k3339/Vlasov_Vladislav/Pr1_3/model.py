from datetime import datetime
from enum import Enum
from typing import Optional

#from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class ConditionType(Enum):
    good = "good"
    normal = "normal"
    bad = "bad"


class BookStatusType(Enum):
    available = "available"
    reserved = "reserved"


class ExchangeStatusType(Enum):
    completed = "completed"
    pending = "pending"
    canceled = "canceled"


class DirectionType(Enum):
    given = "given"
    received = "received"


class ExchangeItem(SQLModel, table=True):
    exchange_id: int = Field(foreign_key="exchange.id", primary_key=True, ondelete="CASCADE")
    book_id: int = Field(foreign_key="book.id", primary_key=True, ondelete="CASCADE")
    direction: DirectionType


class BookDefault(SQLModel):
    title: str
    author: str
    year: int
    condition: ConditionType
    genre: str
    language: str
    description: str
    status: BookStatusType = Field(default=BookStatusType.available)


class Book(BookDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    owner_id: int|None = Field(foreign_key="account.id")

    owner: "Account" = Relationship(back_populates="books")
    exchange_items: Optional[list["Exchange"]] = Relationship(back_populates="items", link_model=ExchangeItem, sa_relationship_kwargs={})


class ProfileDefault(SQLModel):
    full_name: str = Field(default="")
    city: str = Field(default="")
    about: str = Field(default="")
    account_id: int = Field(foreign_key="account.id", ondelete="CASCADE")


class Profile(ProfileDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    account: "Account" = Relationship(
        back_populates="profile",
    )


class AccountDefault(SQLModel):
    login: str
    password: str
    email: str


class ResponseAccountProfile(AccountDefault):
     profile: Optional["Profile"] = None


class Account(AccountDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    profile: Optional["Profile"] = Relationship(back_populates="account", sa_relationship_kwargs={})

    books: Optional[list["Book"]] = Relationship(back_populates="owner")
    sent_exchanges: Optional[list["Exchange"]] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "Exchange.sender_id"}
    )
    received_exchanges: Optional[list["Exchange"]] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={"foreign_keys": "Exchange.receiver_id"}
    )


class ExchangeDefault(SQLModel):
    date: datetime = Field(default_factory=datetime.now)
    status: ExchangeStatusType
    
    sender_id: int = Field(foreign_key="account.id", ondelete="CASCADE")
    receiver_id: int = Field(foreign_key="account.id", ondelete="CASCADE")


class ResponseExchangeBook(ExchangeDefault):
     items: Optional[list["Book"]] = []


class Exchange(ExchangeDefault, table=True):
    id: int = Field(primary_key=True)
    
    sender: "Account" = Relationship(
        back_populates="sent_exchanges",
        sa_relationship_kwargs={"foreign_keys": "Exchange.sender_id"}
    )
    receiver: "Account" = Relationship(
        back_populates="received_exchanges",
        sa_relationship_kwargs={"foreign_keys": "Exchange.receiver_id"}
    )

    items: Optional[list["Book"]] = Relationship(back_populates="exchange_items", link_model=ExchangeItem)