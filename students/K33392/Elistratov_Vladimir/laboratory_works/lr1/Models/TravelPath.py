from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TravelPathDefault(SQLModel):
    travel_id: int = Field(default=None, foreign_key="travel.id")
    pathPoint: str
    pointNumInPath: int = Field(default=0)


class TravelPath(TravelPathDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    _travel: Optional["Travel"] = Relationship(back_populates="_path")
