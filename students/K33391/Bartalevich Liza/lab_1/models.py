import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Rating(Enum):
    five = '5'
    four = '4'
    three = '3'
    two = '2'
    one = '1'
    

class Work(Enum):
    it = 'IT'
    economics = 'economics'
    social = 'social'
    art = 'art'
    freelance = 'freelance' 


class LandmarkDefault(SQLModel):
    name: str
    description: str
    region_id: Optional[int] = Field(default=None, foreign_key="region.id")


class LandmarkShow(LandmarkDefault):
    landmark_rating: Rating = None
    region: Optional["Region"] = None


class Landmark(LandmarkDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    Landmark_rating: Rating
    region: Optional["Region"] = Relationship(back_populates="landmarks")


class RegionDefault(SQLModel):
    name: str
    description: str


class RegionShow(RegionDefault):
    landmarks: Optional[List["Landmark"]] = None


class Region(RegionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    landmarks: Optional[List["Landmark"]] = Relationship(back_populates="region",
                                                         sa_relationship_kwargs={
                                                             "cascade": "all, delete",
                                                         }
                                                   )
    from_location: Optional["Travel"] = Relationship(back_populates="location_from",
                                                     sa_relationship_kwargs=
                                                     dict(foreign_keys="[Travel.location_from_id]"),
                                                     )

    to_location: Optional["Travel"] = Relationship(back_populates="location_to",
                                                   sa_relationship_kwargs=
                                                   dict(foreign_keys="[Travel.location_from_id]"),
                                                   )
    

class CompanionDefault(SQLModel):
    comment: str
    travel_id: Optional[int] = Field(default=None, foreign_key="travel.id")
    traveller_id: Optional[int] = Field(default=None, foreign_key="user.id")


class CompanionShow(CompanionDefault):
    travels: Optional["Travel"] = None
    travellers: Optional["User"] = None


class Companion(CompanionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    travels: Optional["Travel"] = Relationship(back_populates="companions")
    travellers: Optional["User"] = Relationship(back_populates="companions")


class TravelDefault(SQLModel):
    location_from_id: Optional[int] = Field(default=None, foreign_key="region.id")
    location_to_id: Optional[int] = Field(default=None, foreign_key="region.id")
    path_description: str
    date_start:  datetime.datetime
    date_end:  datetime.datetime


class TravelShow(TravelDefault):
    location_from: Optional["Region"] = None
    location_to: Optional["Region"] = None


class Travel(TravelDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    location_from: Optional["Region"] = Relationship(back_populates="from_location",
                                                     sa_relationship_kwargs=
                                                     dict(foreign_keys="[Travel.location_from_id]"),
                                                     )
    location_to: Optional["Region"] = Relationship(back_populates="to_location",
                                                   sa_relationship_kwargs=
                                                   dict(foreign_keys="[Travel.location_to_id]"),
                                                   )

    travellers: Optional[List["User"]] = Relationship(
        back_populates="travels", link_model=Companion
    )
    companions: Optional[List["Companion"]] = Relationship(back_populates="travels")


class UserDefault(SQLModel):
    username: str
    password: str
    email: str
    description: str
    work: Work

class UserLogin(SQLModel):
    username: str
    password: str

class UserShow(UserDefault):
    travels: Optional[List["Travel"]] = None
    companions: Optional[List["Companion"]] = None


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    travels: Optional[List["Travel"]] = Relationship(
        back_populates="travellers", link_model=Companion
    )
    companions: Optional[List["Companion"]] = Relationship(back_populates="travellers")


class ChangePassword(SQLModel):
    old_password: str
    new_password: str
