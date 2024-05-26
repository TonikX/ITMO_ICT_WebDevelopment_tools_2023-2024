from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

"""
if TYPE_CHECKING:
    from models.user_models import User
    from models.step_models import Step
from models.trip_models import UserTripLink

from models_dir.user_models import User
from models_dir.step_models import Step
"""


class StatusType(Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class TripDefault(SQLModel):
    status: StatusType = StatusType.open
    member_capacity: Optional[int] = Field(default=None, ge=0)
    

class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    members: Optional[List["UserTripLink"]] = Relationship(back_populates="trip", 
                                                           sa_relationship_kwargs={"cascade": "all, delete"})
    steps: Optional[List["Step"]] = Relationship(back_populates="trip", 
                                                 sa_relationship_kwargs={"cascade": "all, delete"})

class TripDetailed(TripDefault):
    members: Optional[List["UserTripLinkUsers"]] = None
    steps: Optional[List["StepDetailed"]] = None


from .stay_models import Stay
from .transition_models import Transition
from .step_models import Step, StepDetailed
from .usertriplink_models import UserTripLink, UserTripLinkUsers
Trip.model_rebuild(_types_namespace={"Step": Step, "UserTripLink": UserTripLink})
TripDetailed.model_rebuild(_types_namespace={"UserTripLinkUsers": UserTripLinkUsers, 
                                             "StepDetailed": StepDetailed, 
                                             "Stay": Stay, "Transition": Transition})