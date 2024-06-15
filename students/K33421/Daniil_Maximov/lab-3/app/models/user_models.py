import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional, List



class UserDefault(SQLModel):
    username: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    age: int = Field(ge=0, le=100)


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str = Field(min_length=4, max_length=60)
    is_admin: bool = False
    registered: datetime.datetime = datetime.datetime.now()
    trips: Optional[List["UserTripLink"]] = Relationship(back_populates="user",
                                                         sa_relationship_kwargs={"cascade": "all, delete"})


class UserInput(SQLModel):
    username: str = Field(index=True, unique=True)
    password: str = Field(min_length=4, max_length=60)
    first_name: str
    last_name: str
    age: int = Field(ge=0, le=130)
    is_admin: bool = False


class UserLogin(SQLModel):
    username: str = Field(index=True, unique=True)
    password: str = Field(min_length=4, max_length=60)


class UserPwd(SQLModel):
    old_password: str = Field(min_length=4, max_length=60)
    new_password: str = Field(min_length=4, max_length=60)
    new_password2: str = Field(min_length=4, max_length=60)


from models.user_trip_link_models import UserTripLink
