import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TypeOfTravel(Enum):
    elite_hotel = "elite_hotel"
    pretty_simple_hotel = "pretty_simple_hotel"
    apartments = "apartments"
    tents = "tents"


class PlaceRating(Enum):
    five = '5'
    four = '4'
    three = '3'
    two = '2'
    one = '1'
    zero = '0'


class PlaceBase(SQLModel):
    name: str
    description: str
    place_rating: PlaceRating
    area_id: Optional[int] = Field(default=None, foreign_key="area.id")


class PlaceShow(PlaceBase):
    area: Optional["Area"] = None


class Place(PlaceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    area: Optional["Area"] = Relationship(back_populates="places")


class AreaBase(SQLModel):
    name: str
    description: str


class AreaShow(AreaBase):
    places: Optional[List["Place"]] = None


class Area(AreaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    places: Optional[List["Place"]] = Relationship(back_populates="area",
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


class TravelTogetherBase(SQLModel):
    comment: str
    travel_id: Optional[int] = Field(default=None, foreign_key="travel.id")
    traveller_id: Optional[int] = Field(default=None, foreign_key="user.id")


class TravelTogetherShow(TravelTogetherBase):
    travels: Optional["Travel"] = None
    travellers: Optional["User"] = None


class TravelTogether(TravelTogetherBase, table=True):
    id: int = Field(default=None, primary_key=True)
    travels: Optional["Travel"] = Relationship(back_populates="traveltogethers")
    travellers: Optional["User"] = Relationship(back_populates="traveltogethers")


class TravelBase(SQLModel):
    location_from_id: Optional[int] = Field(default=None, foreign_key="area.id")
    location_to_id: Optional[int] = Field(default=None, foreign_key="area.id")
    path_description: str
    date_start:  datetime.datetime
    date_end:  datetime.datetime
    type_of_travel: TypeOfTravel


class TravelShow(TravelBase):
    location_from: Optional["Area"] = None
    location_to: Optional["Area"] = None


class Travel(TravelBase, table=True):
    id: int = Field(default=None, primary_key=True)
    location_from: Optional["Area"] = Relationship(back_populates="from_location",
                                                   sa_relationship_kwargs=
                                                   dict(foreign_keys="[Travel.location_from_id]"),
                                                   )
    location_to: Optional["Area"] = Relationship(back_populates="to_location",
                                                 sa_relationship_kwargs=
                                                 dict(foreign_keys="[Travel.location_to_id]"),
                                                 )

    travellers: Optional[List["User"]] = Relationship(
        back_populates="travels", link_model=TravelTogether
    )
    traveltogethers: Optional[List["TravelTogether"]] = Relationship(back_populates="travels")


class UserBase(SQLModel):
    username: str
    password: str


class UserShow(UserBase):
    travels: Optional[List["Travel"]] = None
    traveltogethers: Optional[List["TravelTogether"]] = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    travels: Optional[List["Travel"]] = Relationship(
        back_populates="travellers", link_model=TravelTogether
    )
    traveltogethers: Optional[List["TravelTogether"]] = Relationship(back_populates="travellers")
