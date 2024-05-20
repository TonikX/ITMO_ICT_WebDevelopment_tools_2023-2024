from enum import Enum
from typing import Optional, List
from datetime import date

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class Genres(Enum):
    fantasy = "fantasy"
    detectives = "detectives"
    romance = "romance"
    thrillers = "thrillers"
    horrors = "horrors"
    comics = "comics"
    adventures = "adventures"
    poetry = "poetry"
    other = "other"


class ReadingStatus(Enum):
    exchanged = "exchanged"
    in_process = "in_process"
    available = "available"


class RequestStatus(Enum):
    sent = "sent"
    accepted = "accepted"
    rejected = "rejected"


class Readings(SQLModel, table=True):
    #id: int = Field(default=None, primary_key=True)
    reader_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="books.id", primary_key=True)
    status: ReadingStatus
    start_date: date = Field(default=date.today)
    end_date: date = Field(nullable=True)

    reader: Optional["Users"] = Relationship(back_populates="readings")
    book: Optional["Books"] = Relationship(back_populates="book_read")


class Users(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    name: str
    surname: str
    email: str
    country: str
    city: str

    book_ownership: List["Books"] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="owner")

    reader: List["Books"] = Relationship(back_populates="in_readings", link_model=Readings)
    readings: List["Readings"] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="reader")

    reviews: List["Review"] = Relationship(back_populates="reviewer")

    __table_args__ = {"extend_existing": True}
    #exchange_requests_sent: List["Requests"] = Relationship(back_populates="sender")
    #exchange_requests_received: List["Requests"] = Relationship(back_populates="recipient")


class Books(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    genre: Genres
    publisher: str
    year_of_publication: int
    description: str

    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    owner: Optional[Users] = Relationship(back_populates="book_ownership")

    in_readings: List["Users"] = Relationship(back_populates="reader", link_model=Readings)
    book_read: List["Readings"] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="book")

    reviews: List["Review"] = Relationship(sa_relationship_kwargs={"cascade": "delete"}, back_populates="book")
    book_request: List["Requests"] = Relationship(back_populates="book")

    __table_args__ = {"extend_existing": True}


class Requests(SQLModel, table=True):
    #id: int = Field(default=None, primary_key=True)
    receiver_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    sender_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="books.id", primary_key=True)
    conditions: Optional[str]
    response: Optional[str] = None
    status: RequestStatus
    #sender: Optional[Users] = Relationship(back_populates="exchange_requests_sent", link_model=Users)
    sender: Optional[Users] = Relationship(sa_relationship_kwargs=dict(foreign_keys="[Requests.sender_id]"))
    #recipient: Optional[Users] = Relationship(back_populates="exchange_requests_received", link_model=Users)
    recipient: Optional[Users] = Relationship(sa_relationship_kwargs=dict(foreign_keys="[Requests.receiver_id]"))
    book: Optional[Books] = Relationship(back_populates="book_request")


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="books.id")
    reviewer_id: int = Field(foreign_key="users.id")
    rating: int  # Assuming a rating scale of 1-5
    comment: Optional[str] = None

    book: Optional[Books] = Relationship(back_populates="reviews")
    reviewer: Optional[Users] = Relationship(back_populates="reviews")

    __table_args__ = {"extend_existing": True}


'--------------pydantic models------------------'


class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    country: str
    city: str


class UsersRegistration(UserBase):
    username: str
    hashed_password: str


class UserGet(UserBase):

    book_ownership: List["Books"] = []
    reader: List["Books"] = []

    class Config:
        orm_mode = True


class User(UsersRegistration):
    id: Optional[int]
    book_ownership: List["BooksPost"] = []
    reader: List["BooksPost"] = []
    reviews: List["ReviewsGet"] = []

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):

    rating: int
    comment: Optional[str] = None


class ReviewsGet(ReviewBase):
    id: Optional[int]
    book: "BooksPost"#Optional[Books]
    reviewer: UserBase#Optional[Users]

    class Config:
        orm_mode = True


class BooksPost(BaseModel):
    title: str
    author: str
    genre: Genres
    publisher: str
    year_of_publication: int
    description: str


class MyBooksBase(BooksPost):
    id: Optional[int]
    reviews: List["Review"] = []

    class Config:
        orm_mode = True


class BooksBase(MyBooksBase):
    owner: UserBase
    book_read: List["ReadingRead"] = []

    class Config:
        orm_mode = True


class ReadingRead(BaseModel):

    reader: UserBase
    book: BooksPost
    status: ReadingStatus
    start_date: date
    end_date: Optional[date] = None

    class Config:
        orm_mode = True


class ReadingPost(BaseModel):

    status: ReadingStatus
    start_date: date


class BaseRequest(BaseModel):

    conditions: Optional[str]


class UpdateRequest(BaseRequest):

    status: RequestStatus
    response: Optional[str]


class GetRequest(UpdateRequest):

    book: Optional[Books]
    sender: Optional[Users]
    recipient: Optional[Users]

    class Config:
        orm_mode = True





