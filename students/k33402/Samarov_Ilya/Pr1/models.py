import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class PlaceRating(Enum):
    five = '5'
    four = '4'
    three = '3'
    two = '2'
    one = '1'
    zero = '0'


class Place(BaseModel):
    id: int
    name: str
    description: str
    place_rating: PlaceRating


class Area(BaseModel):
    id: int
    name: str
    description: str
    places: Optional[List["Place"]] = []
