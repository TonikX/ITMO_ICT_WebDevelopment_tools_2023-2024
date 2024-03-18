from typing import List, Optional
from pydantic import BaseModel


class Organizer(BaseModel):
    name: str
    contact_email: str


class Task(BaseModel):
    task_id: int
    title: str
    description: str
    requirements: str
    evaluation_criteria: str


class Hackathon(BaseModel):
    hackathon_id: int
    title: str
    description: str
    start_date: str
    end_date: str
    organizer: Organizer
    tasks: List[Task]


class HackathonCreate(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str
    organizer: Organizer
    tasks: List[Task]


class HackathonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    organizer: Optional[Organizer] = None
    tasks: Optional[List[Task]] = None
