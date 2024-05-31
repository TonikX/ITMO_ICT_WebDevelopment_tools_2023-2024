from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from Models.Enum import States


class TravelUsersLinkDefault(SQLModel):
    travel_id: Optional[int] = Field(
        default=None, foreign_key="travel.id", primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )


class TravelUsersLinkState(TravelUsersLinkDefault):
    state: States = Field(default=States.awaiting)


class TravelUsersLink(TravelUsersLinkState, table=True):
    joinDate: datetime = Field(default=datetime.now())