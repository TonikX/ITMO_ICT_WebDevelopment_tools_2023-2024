from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel):
    username: str
    email: str
    password_hash: str

    def hash_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)


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


class WorkExperienceBase(SQLModel):
    organization: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
