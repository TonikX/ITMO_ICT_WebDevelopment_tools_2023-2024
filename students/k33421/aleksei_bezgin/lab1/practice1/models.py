from enum import Enum
from typing import Optional, List

from pydantic import BaseModel
from typing_extensions import TypedDict



class Profession(BaseModel):
    id: int
    title: str
    description: str


class Skill(BaseModel):
    id: int
    name: str
    description: str


class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class Warrior(BaseModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession: Profession
    skills: Optional[List[Skill]] = []
