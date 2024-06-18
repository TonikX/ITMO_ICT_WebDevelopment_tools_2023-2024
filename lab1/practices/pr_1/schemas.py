import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class Rating(Enum):
    necessary = 'necessary'
    may_be = 'may_be'
    stupid = 'stupid'


class Waste(BaseModel):
    id: int
    name: str
    value: float
    rating: Rating



class Category(BaseModel):
    id: int
    name: str
    wastes: Optional[List["Waste"]] = []
