# Data Models

The application utilizes the following data models:

## Person
```python
class Person(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    age: Optional[int]
    profile: Optional["Profile"] = Relationship(back_populates='profile_owner')
    books: Optional[List["Book"]] = Relationship(link_model=BookOwnership, back_populates='owners')

```
## Profile
```python
class Profile(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    nickname: Optional[str]
    hobbies: Optional[str]
    skills: Optional[str]
    profile_owner: Optional["Person"] = Relationship(back_populates="profile")
```

## Book
``` py
class Book(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    title: str
    author: str
    owners: Optional[List[Person]] = Relationship(link_model=BookOwnership, back_populates='books')
```

## Book Ownership 
``` py
class BookOwnership(SQLModel, table=True):
    book_id: Optional[int] = Field(primary_key=True, foreign_key='book.id')
    person_id: Optional[int] = Field(primary_key=True, foreign_key='person.id')
    status: BookStatus
    edition: int = None
    level: int | None
```

## Request
```python 
class Request(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    sender_id: int = Field(foreign_key='person.id')
    reciever_id: int = Field(foreign_key='person.id')
    book_id: int = Field(foreign_key='book.id')
    status: RequestStatus | None
    sender: Optional[Person] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Request.sender_id]"})
    receiver: Optional[Person] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Request.reciever_id]"})
    book: Optional[Book] = Relationship()
```
