from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

### Base Models ###


class BookBase(SQLModel):
    name: str
    author: str
    publication_year: int
    description: Optional[str] = None


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class RequestStatus(str, Enum):
    pending = "pending"
    rejected = "rejected"
    approved = "approved"


### Many-to-many Models ###


class Book(BookBase, SQLModel):
    id: int = Field(primary_key=True)
    owner_id: int = Field(foreign_key="reader.id")
    available: bool = True
    requests: List["Request"] = Relationship()


class Reader(SQLModel):
    id: int = Field(primary_key=True)
    name: str
    surname: str
    age: int
    gender: Gender
    books: List[Book] = Relationship(back_populates="owner")
    received_books: List["Request"] = Relationship(back_populates="receiver")
    sent_requests: List["Request"] = Relationship(back_populates="sender")


class Request(SQLModel):
    id: int = Field(primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    sender_id: int = Field(foreign_key="reader.id")
    receiver_id: int = Field(foreign_key="reader.id")
    status: RequestStatus = RequestStatus.pending
    created_at: datetime = Field(default=datetime.utcnow)

    book: Book = Relationship(back_populates="requests")
    sender: Reader = Relationship(back_populates="sent_requests")
    receiver: Reader = Relationship(back_populates="received_books")

    def approve(self):
        self.status = RequestStatus.approved

    def reject(self):
        self.status = RequestStatus.rejected
