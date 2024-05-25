from datetime import date
from typing import Optional, List
from pydantic import BaseModel
from models import Users, Books, Readings, Genres, ReadingStatus, Review, RequestStatus


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





