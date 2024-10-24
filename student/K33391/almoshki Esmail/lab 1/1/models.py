from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class BookStatus(Enum):
    available = "available"
    on_rental = "on_rental"


class RequestStatus(Enum):
    accepted = "accepted"
    declined = "declined"


class Person(BaseModel):
    id: int
    name: str
    age: int
    profile: Optional["Profile"]
    Books: Optional['Book']


class Profile(BaseModel):
    id: int
    nickname: str
    hobbies: str
    skills: str


class Book(BaseModel):
    id: int
    title: str
    author: str
    edition: int


class BookOwnership(BaseModel):
    book_id: int
    person_id: int
    status: BookStatus


class Request(BaseModel):
    id: int
    sender_id: int
    reciever_id: int
    book_id: int
    status: RequestStatus
