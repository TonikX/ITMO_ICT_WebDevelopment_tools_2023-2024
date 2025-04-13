from enum import Enum

from pydantic import BaseModel

class ConditionType(Enum):
    good = "good"
    normal = "normal"
    bad = "bad"

class StatusType(Enum):
    available = "available"
    reserved = "reserved"
    

class Profile(BaseModel):
    id: int
    full_name: str
    city: str
    about: str

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    condition: ConditionType
    genre: str
    language: str
    description: str
    status: StatusType

class Account(BaseModel):
    id: int
    login: str
    password: str
    email: str
    profile: Profile
    books: list[Book]|None = []