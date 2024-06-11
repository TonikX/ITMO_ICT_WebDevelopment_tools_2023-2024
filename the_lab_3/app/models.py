from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .base_models import *


class BookOwnership(SQLModel, table=True):
    book_id: Optional[int] = Field(
        default=None, foreign_key="book.id", primary_key=True
    )
    owner_id: Optional[int] = Field(
        default=None, foreign_key="reader.id", primary_key=True
    )
    book: Optional["Book"] = Relationship(back_populates="ownerships")
    owner: Optional["Reader"] = Relationship(back_populates="ownerships")

    class Config:
        orm_mode = True


class BookGenreLink(SQLModel, table=True):
    book_id: Optional[int] = Field(
        default=None, foreign_key="book.id", primary_key=True
    )
    genre_id: Optional[int] = Field(
        default=None, foreign_key="genre.id", primary_key=True
    )
    book: Optional["Book"] = Relationship(back_populates="genre_links")
    genre: Optional["Genre"] = Relationship(back_populates="book_links")

    class Config:
        from_attributes = True


class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    books: List["Book"] = Relationship(
        back_populates="genres", link_model=BookGenreLink
    )
    book_links: List["BookGenreLink"] = Relationship(back_populates="genre")

    class Config:
        from_attributes = True


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    available: bool = Field(default=True)
    readers: List["Reader"] = Relationship(
        back_populates="books", link_model=BookOwnership
    )
    ownerships: List[BookOwnership] = Relationship(back_populates="book")
    genres: List[Genre] = Relationship(back_populates="books", link_model=BookGenreLink)
    genre_links: List[BookGenreLink] = Relationship(back_populates="book")

    class Config:
        orm_mode = True


class WorkExperience(WorkExperienceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reader_id: int = Field(foreign_key="reader.id")
    reader: Optional["Reader"] = Relationship(back_populates="work_experience")

    class Config:
        orm_mode = True


class Reader(User, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    age: int
    gender: Gender
    profile_description: Optional[str] = None
    work_experience: List[WorkExperience] = Relationship(back_populates="reader")
    books: List[Book] = Relationship(back_populates="readers", link_model=BookOwnership)
    ownerships: List[BookOwnership] = Relationship(back_populates="owner")

    class Config:
        orm_mode = True


class UserRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    sender_id: int = Field(foreign_key="reader.id")
    receiver_id: int = Field(foreign_key="reader.id")
    status: RequestStatus = Field(default=RequestStatus.pending)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def approve(self):
        self.status = RequestStatus.approved
        self.updated_at = datetime.utcnow()

    def reject(self):
        self.status = RequestStatus.rejected
        self.updated_at = datetime.utcnow()

    class Config:
        orm_mode = True


class ReaderResponse(SQLModel):
    id: int
    username: str
    email: str
    name: str
    surname: str
    age: int
    gender: Gender
    profile_description: Optional[str] = None
    books: List[BookBase] = []
    work_experience: List[WorkExperienceBase] = []

    class Config:
        orm_mode = True


class BookOwnershipResponse(SQLModel):
    book: Book
    owner: ReaderResponse

    class Config:
        orm_mode = True


class BookResponse(SQLModel):
    id: int
    name: str
    author: str
    publication_year: int
    description: Optional[str] = None
    available: bool
    genres: List[Genre] = []

    class Config:
        orm_mode = True


User.model_rebuild()
Book.model_rebuild()
Reader.model_rebuild()
UserRequest.model_rebuild()
BookOwnership.model_rebuild()
WorkExperience.model_rebuild()
BookGenreLink.model_rebuild()
Genre.model_rebuild()
