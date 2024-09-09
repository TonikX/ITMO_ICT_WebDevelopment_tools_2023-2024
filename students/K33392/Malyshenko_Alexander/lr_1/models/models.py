from datetime import datetime
from enum import Enum
from typing import Optional, List

# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


# region Links
class UserTravelLinkDefault(SQLModel):
    user_id: Optional[int] = Field(foreign_key="user.id", primary_key=True, default=None)
    travel_id: Optional[int] = Field(foreign_key="travel.id", primary_key=True, default=None)


class UserTravelLink(UserTravelLinkDefault, table=True):
    is_leader: bool = Field(default=False)
    join_date: datetime = Field(default=datetime.now())
# endregion


# region Skills
class UserSkillDefault(SQLModel):
    user_id: Optional[int] = Field(foreign_key="user.id", default=None)
    description: str = Field(max_length=100)
    experience: float = Field(ge=0)


class UserSkill(UserSkillDefault, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

    _user: Optional["User"] = Relationship(back_populates="_skills")
# endregion


# region User
class UserDefault(SQLModel):
    username: str = Field(max_length=20, unique=True)
    email: str = Field(max_length=50, unique=True)


class UserPassword(UserDefault):
    password: str


class User(UserPassword, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

    _skills: Optional[List[UserSkill]] = Relationship(back_populates="_user")
    _travels: Optional[List["Travel"]] = Relationship(back_populates="_users", link_model=UserTravelLink)


# endregion


# region Travel
class TravelDefault(SQLModel):
    description: str = Field(max_length=100)
    start_date: datetime = Field(default=datetime.now())
    end_date: datetime = Field(default=datetime.now())


class Travel(TravelDefault, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

    _users: Optional[List[User]] = Relationship(back_populates="_travels", link_model=UserTravelLink)
    _route: Optional["TravelRoute"] = Relationship(back_populates="_travel")
# endregion


# region Travel route
class TravelRouteDefault(SQLModel):
    description: str = Field(max_length=100)
    travel_id: Optional[int] = Field(foreign_key="travel.id", default=None)


class TravelRoute(TravelRouteDefault, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

    _travel: Optional[Travel] = Relationship(back_populates="_route")
    _points: Optional[List["TravelPoint"]] = Relationship(back_populates="_route")
# endregion


# region Travel points
class TravelPointDefault(SQLModel):
    travel_route_id: Optional[int] = Field(foreign_key="travelroute.id", default=None)
    name: str = Field(max_length=100)


class TravelPoint(TravelPointDefault, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

    _route: Optional[TravelRoute] = Relationship(back_populates="_points")
# endregion
