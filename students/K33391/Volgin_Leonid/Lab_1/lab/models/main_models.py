from typing import Optional
from sqlmodel import SQLModel, Field, Relationship



class Author_Default(SQLModel):
    name: str
    info: str

class Author(Author_Default, table=True):
    #__table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None,primary_key=True)
    books: list['Book'] = Relationship(back_populates='author')


class WishList_Default(SQLModel):
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)

class Acception(SQLModel):
    is_accepted: Optional[bool] = Field(default=None, nullable=True)

class WishList(WishList_Default, table=True):
    #__table_args__ = {'extend_existing': True}
    #id: Optional[int] = Field(primary_key=True)
    is_accepted: Optional[bool] = Field(default=None, nullable=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)



class User_Default(SQLModel):
    username: str = Field(index=True)
    password: str
    email: str
    description: str

class User(User_Default, table=True):
    #__table_args__ = {'extend_existing': True}
    id: int = Field(default=None,primary_key=True)
    user_books: list['Book'] = Relationship(back_populates='user')
    books: list['Book'] = Relationship(back_populates="users", link_model=WishList)


class Publisher_Default(SQLModel):
    name: str
    info: str

class Publisher(Publisher_Default, table=True):
    #__table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None,primary_key=True)
    books: list['Book'] = Relationship(back_populates='publisher')


class Book_Default(SQLModel):
    name: str
    description: str

class Book(Book_Default, table=True):
    #__table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(primary_key=True)

    user_id: int = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="user_books")

    author_id: int = Field(default=None, nullable=True, foreign_key="author.id")
    author: Optional[Author] = Relationship(back_populates="books")

    publisher_id: int = Field(default=None, nullable=True, foreign_key="publisher.id")
    publisher: Optional[Publisher] = Relationship(back_populates="books")

    users: list[User] = Relationship(back_populates="books", link_model=WishList)







