import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional, List


class GenderType(Enum):
    undefined = "-"
    female = "f"
    male = "m"


class UserDefault(SQLModel):
    username: str = Field(index=True, unique=True)
    gender: GenderType = "-"
    age: int = Field(ge=0, le=100)
    phone: str = Field(regex="\+?\d{7,11}")

class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str = Field(min_length=4, max_length=60)
    registered: datetime.datetime = datetime.datetime.now()
    trips: Optional[List["UserTripLink"]] = Relationship(back_populates="user",
                                                         sa_relationship_kwargs={"cascade": "all, delete"})

class UserLogin(SQLModel):
    username: str = Field(index=True, unique=True)
    password: str = Field(min_length=4, max_length=60)


from models.user_trip_link_models import UserTripLink
User.model_rebuild(_types_namespace={"UserTripLink": UserTripLink})