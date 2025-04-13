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


#m2m

class ExchangeItem(SQLModel, table=True):
    exchange_id: int = Field(default=None, foreign_key="exchange.id", primary_key=True, ondelete="CASCADE")
    book_id: int = Field(default=None, foreign_key="book.id", primary_key=True, ondelete="CASCADE")
    direction: DirectionType


#Book

class BookDefault(SQLModel):
    owner_id: int
    title: str
    author: str|None
    year: int|None
    condition: ConditionType
    genre: str|None
    language: str|None
    description: str|None
    status: BookStatusType = Field(default=BookStatusType.available)


class BookUpdate(SQLModel):
    owner_id: int|None = None
    title: str|None = None
    author: str|None = None
    year: int|None = None
    condition: ConditionType|None = None
    genre: str|None = None
    language: str|None = None
    description: str|None = None
    status: BookStatusType|None = None


class Book(BookDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    owner_id: int|None = Field(foreign_key="account.id")

    owner: Optional["Account"] = Relationship(back_populates="books")
    exchange_items: Optional[list["Exchange"]] = Relationship(back_populates="items", link_model=ExchangeItem, sa_relationship_kwargs={"cascade": "all, delete"})


#Exchange

class ExchangeDefault(SQLModel):
    date: datetime = Field(default_factory=datetime.now)
    status: ExchangeStatusType = Field(default=ExchangeStatusType.pending)
    
    sender_id: int = Field(foreign_key="account.id", ondelete="CASCADE")
    receiver_id: int = Field(foreign_key="account.id", ondelete="CASCADE")


class ExchangeItemCreate(SQLModel):
    book_id: int
    direction: DirectionType


class ExchangeCreate(ExchangeDefault):
    items: list["ExchangeItemCreate"] = []


class ResponseExchangeBook(ExchangeDefault):
    id: int
    items: list["Book"] = []


class BooksChange(SQLModel):
    deleted_books: list["ExchangeItemCreate"] = []
    new_books: list["ExchangeItemCreate"] = []


class Exchange(ExchangeDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    
    sender: "Account" = Relationship(
        back_populates="sent_exchanges",
        sa_relationship_kwargs={"foreign_keys": "Exchange.sender_id"}
    )
    receiver: "Account" = Relationship(
        back_populates="received_exchanges",
        sa_relationship_kwargs={"foreign_keys": "Exchange.receiver_id"}
    )

    items: Optional[list["Book"]] = Relationship(back_populates="exchange_items", link_model=ExchangeItem, sa_relationship_kwargs={"cascade": "all, delete"})