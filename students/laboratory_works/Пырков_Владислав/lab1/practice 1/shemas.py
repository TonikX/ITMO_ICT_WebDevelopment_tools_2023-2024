from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

class Participant(BaseModel):
    id: int
    username: str
    email: str
    password: str
    contact_number: str


class Team(BaseModel):
    id: int
    name: str
    description: str
    participants: Optional[List[Participant]] = []
