from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, select, Column
from typing import Optional, List
from enum import Enum




class BookStatus(Enum,):
    available = "available"
    on_rental = "on_rental"


# TODO solve the Hierachial serialization problem
class RequestStatus(Enum):
    accepted = "accepted"
    declined = "declined"
    pending = "pending"

class BookOwnershipResponse(SQLModel):
    person_info: Optional["PersonResponse"] = None  
    book_info: Optional["BookResponse"] = None     
    status: BookStatus
    edition: Optional[int] = None


# class DefaultBookOwnership(SQLModel):
    
    
class BookOwnership(SQLModel, table=True):
    book_id: Optional[int] = Field(primary_key=True, foreign_key='book.id')
    person_id: Optional[int] = Field(primary_key=True, foreign_key='person.id')
    status: BookStatus 
    edition: int =  None 
    level: int | None
    # book: Optional['Book'] = Relationship()  # Corrected
    # person: Optional['Person'] = Relationship(sa_relationship_kwargs={"foreign_keys": ['']})  # Corrected




class DefaultPerson(SQLModel):
    name: str
    age: Optional[int]
    # profile_id: int | None = Field(default= None, foreign_key='profile.id')

class Person(DefaultPerson, table=True):
    id: Optional[int]  = Field(primary_key=True, default=None)
    profile: Optional["Profile"] = Relationship(back_populates='profile_owner')
    books: Optional[List["Book"]] = Relationship(link_model=BookOwnership, back_populates='owners')
    

class DefaultProfile(SQLModel):
    nickname: str | None
    hobbies: str | None
    skills: str | None
    person_id : int | None = Field(foreign_key= "person.id", default= None)


class Profile(DefaultProfile,  table=True):
    id: Optional[int]  = Field(primary_key=True, default=None)
    profile_owner: Optional["Person"] = Relationship(back_populates="profile")
    

class DefaultBook(SQLModel):    
    title: str
    author: str



class Book(DefaultBook , table= True):
    id: int = Field(primary_key= True, default= None)
    owners: Optional[List[Person]] = Relationship(link_model=BookOwnership, back_populates='books')

class BookOwners(DefaultBook):
    owners: Optional[List[Person]] = None
  
class PersonProfile(DefaultPerson):
    profile : Optional[Profile] = None
    books: Optional[List[Book]] = None





class PersonResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None

    class Config:
        orm_mode = True

class BookResponse(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True

class RequestResponse(BaseModel):
    id: int
    sender: PersonResponse
    receiver: PersonResponse
    book: BookResponse
    status: RequestStatus


class DefaultRequest(SQLModel):
    sender_id: int = Field(foreign_key='person.id')
    reciever_id: int =  Field(foreign_key='person.id')
    book_id: int =  Field(foreign_key='book.id')
    status: RequestStatus | None


    

class Request(DefaultRequest, table = True):
    id: int = Field(primary_key=True, default= None)
    
    sender: Optional[Person] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Request.sender_id]"})
    receiver: Optional[Person] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Request.reciever_id]"})
    book: Optional[Book] = Relationship()  

