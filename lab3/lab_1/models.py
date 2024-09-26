import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class CompanionBase(SQLModel):
    comment: str
    travel_id: Optional[int] = Field(default=None, foreign_key="travel.id")
    traveller_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Companion(CompanionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    travels: Optional["Travel"] = Relationship(back_populates="companions")
    travellers: Optional["User"] = Relationship(back_populates="companions")


class UserBase(SQLModel):
    username: str
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    travels: Optional[List["Travel"]] = Relationship(
        back_populates="travellers", link_model=Companion
    )
    companions: Optional[List["Companion"]] = Relationship(back_populates="travellers")


class TravelBase(SQLModel):
    start_region_id: Optional[int] = Field(default=None, foreign_key="region.id")
    region_region_id: Optional[int] = Field(default=None, foreign_key="region.id")
    path_description: str
    date_start:  datetime.datetime
    date_end:  datetime.datetime


class TravelShow(TravelBase):
    start_region: Optional["Region"] = None
    region_region: Optional["Region"] = None
    travellers: Optional[List["User"]] = None
    companions: Optional[List["Companion"]] = None


class Travel(TravelBase, table=True):
    id: int = Field(default=None, primary_key=True)
    start_region: Optional["Region"] = Relationship(back_populates="start_travel",
                                                     sa_relationship_kwargs=
                                                     dict(foreign_keys="[Travel.start_region_id]"),
                                                     )
    region_region: Optional["Region"] = Relationship(back_populates="end_travel",
                                                   sa_relationship_kwargs=
                                                   dict(foreign_keys="[Travel.region_region_id]"),
                                                   )

    travellers: Optional[List["User"]] = Relationship(
        back_populates="travels", link_model=Companion
    )
    companions: Optional[List["Companion"]] = Relationship(back_populates="travels")


class Rating(Enum):
    five = '5'
    four = '4'
    three = '3'
    two = '2'
    one = '1'


class WhatToSeeBase(SQLModel):
    name: str
    description: str
    rating: Rating
    region_id: Optional[int] = Field(default=None, foreign_key="region.id")


class WhatToSee(WhatToSeeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    region: Optional["Region"] = Relationship(back_populates="whattosees")


class RegionBase(SQLModel):
    name: str


class Region(RegionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    whattosees: Optional[List["WhatToSee"]] = Relationship(back_populates="region",
                                                           sa_relationship_kwargs={
                                                               "cascade": "all, delete",
                                                           }
                                                           )
    start_travel: Optional["Travel"] = Relationship(back_populates="start_region",
                                                     sa_relationship_kwargs=
                                                     dict(foreign_keys="[Travel.start_region_id]"),
                                                     )

    end_travel: Optional["Travel"] = Relationship(back_populates="region_region",
                                                   sa_relationship_kwargs=
                                                   dict(foreign_keys="[Travel.region_region_id]"),
                                                   )


class Site(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    title: str
