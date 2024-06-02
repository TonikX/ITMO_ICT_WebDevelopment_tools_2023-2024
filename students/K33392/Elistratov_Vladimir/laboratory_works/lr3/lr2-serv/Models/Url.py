from typing import Optional, List
from sqlmodel import SQLModel, Field

class Link(SQLModel):
    link: str