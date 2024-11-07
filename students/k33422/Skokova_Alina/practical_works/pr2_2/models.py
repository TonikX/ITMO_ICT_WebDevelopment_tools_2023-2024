from enum import Enum
from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class ConditionType(Enum):
    excellent = "excellent"
    good = "good"
    used = "used"

class RequestStatusType(Enum):
    waiting = "waiting"
    approved = "approved"
    rejected = "rejected"

class RequestDefault(SQLModel):
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    book_id: Optional[int] = Field(default=None, foreign_key="book.book_id")
    request_date: datetime = datetime.now()
    request_status: RequestStatusType

class Request(RequestDefault, table=True):
    request_id: int = Field(default=None, primary_key=True)



class UserDefault(SQLModel):
    user_name: str
    user_email: str
    user_info: str

class User(UserDefault, table=True):
    user_id: int = Field(default=None, primary_key=True)
    libraries: Optional[List["Library"]] = Relationship(back_populates="user", cascade_delete=True)
    books: Optional[List["Book"]] = Relationship(back_populates="users", link_model=Request)

class UserBooks(UserDefault):
    user_id: int
    books: Optional[List["Book"]] = None


class LibraryDefault(SQLModel):
    library_name: str
    user_id: int = Field(default=None, foreign_key="user.user_id", ondelete="CASCADE")

class Library(LibraryDefault, table=True):
    library_id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="libraries")
    books: Optional[List["Book"]] = Relationship(back_populates="library", cascade_delete=True) 

class LibraryUsers(LibraryDefault):
    library_id: int
    user: User



class BookDefault(SQLModel):
    book_name: str
    book_author: str
    book_condition: ConditionType
    library_id: int = Field(default=None, foreign_key="library.library_id", ondelete="CASCADE")

class Book(BookDefault, table=True):
    book_id: int = Field(default=None, primary_key=True)
    library: Library = Relationship(back_populates="books")
    users: Optional[List[User]] = Relationship(back_populates="books", link_model=Request)

class BookLibraries(BookDefault):
    book_id: int
    library: LibraryUsers
    users: Optional[List[User]] = None