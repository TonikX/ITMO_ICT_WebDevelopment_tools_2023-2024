import datetime
from enum import Enum
from typing import Optional, List
from pydantic import EmailStr, validator
from sqlmodel import SQLModel, Field, Relationship, AutoString


class GenderType(Enum):
    undefined = "-"
    female = "f"
    male = "m"


class UserDefault(SQLModel):
    username: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    gender: GenderType = "-"
    age: int = Field(ge=0, le=130)
    telephone: str = Field(regex="\+?\d{7,11}")
    email: EmailStr = Field(sa_type=AutoString)
    bio: Optional[str] = ""


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    password: str = Field(min_length=8, max_length=60)
    registered: datetime.datetime = datetime.datetime.now()
    is_admin: bool = False
    trips: Optional[List["UserTripLink"]] = Relationship(back_populates="user", 
                                                         sa_relationship_kwargs={"cascade": "all, delete"})


class UserInput(SQLModel):
    username: str = Field(index=True, unique=True)
    password: str = Field(min_length=8, max_length=60)
    password2: str = Field(min_length=8, max_length=60)
    first_name: str
    last_name: str
    gender: GenderType = "-"
    age: int = Field(ge=0, le=130)
    telephone: str = Field(regex="\+?\d{7,11}")
    email: EmailStr = Field(sa_type=AutoString)
    bio: Optional[str] = ""

    @validator('password2')
    def check_match(cls, pwd, values, **kwargs):
        if 'password' in values and pwd != values['password']:
            raise ValueError("passwords don't match")
        return pwd


class UserLogin(SQLModel):
    username: str
    password: str


class UserPwd(SQLModel):
    old_password: str = Field(min_length=8, max_length=60)
    new_password: str = Field(min_length=8, max_length=60)
    new_password2: str = Field(min_length=8, max_length=60)


from models.usertriplink_models import UserTripLink
User.model_rebuild(_types_namespace={"UserTripLink": UserTripLink})
