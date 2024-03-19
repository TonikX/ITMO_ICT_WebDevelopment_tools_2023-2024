from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from Models.Links import TravelUsersLink


class TravelDefault(SQLModel):
    sourceCity: str
    destinationCity: str
    startDate: datetime
    leader_id: int = Field(default=None, foreign_key="user.id")
    transport_id: int = Field(default=None, foreign_key="transport.id")


class Travel(TravelDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    _companions: Optional[List["User"]] = Relationship(back_populates="_travelAsPassenger", link_model=TravelUsersLink)
    _leader: Optional["User"] = Relationship(back_populates="_travelsAsLeader")
    _transport: Optional["Transport"] = Relationship(back_populates="_travels")
    _path: Optional[List["TravelPath"]] = Relationship(back_populates="_travel")
