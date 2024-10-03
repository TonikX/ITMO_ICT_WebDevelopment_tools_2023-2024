from enum import Enum
from typing import Optional, List
from datetime import date

from pydantic import BaseModel

class Priority(BaseModel):
    id: int
    name: str

class Tag(BaseModel):
    id: int
    name: str

class Task(BaseModel):
    id: int
    title: str
    description: str
    dueTo: date
    priority_id: int
    tags: Optional[List[Tag]] = []
