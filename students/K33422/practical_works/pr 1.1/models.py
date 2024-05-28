from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

temp_bd = [{
    "id": 1,
    "user": {"id": 1, "username": "karpov"},
    "name": "Мартынов Дмитрий",
    "description": "desc",
    "experience": {
        "year": 2,
        "place": "ООО ФА",
        "description": "Эксперт по всем вопросам"
    },
    "skills": [{"id": 1, "name": "python"}]
},{
    "id": 2,
    "user": {"id": 2, "username": "martynov"},
    "name": "Мартынов Роман",
    "description": "ввв",
    "experience": {
        "year": 3.5,
        "place": "ООО ФА",
        "description": "Эксперт по всем вопросам"
    },
    "skills": [{"id": 1, "name": "python"}]
    },
    ]


class Skill(BaseModel):
    id: int
    name: str

class User(BaseModel):
   id: int
   username: str

class Experience(BaseModel):
    year: float
    place: str
    description: str

class Profile(BaseModel):
    id: int
    user: User
    name: str
    description: str
    skills: Optional[List[Skill]] = []


