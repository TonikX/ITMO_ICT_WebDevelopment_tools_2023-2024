from sqlmodel import Session, select

from Models.Transport import *
from Models.Travel import *
from Models.User import *
from Models.TravelPath import *


class UserDeatails(UserDefault):
    travelsAsLeader: Optional[List[Travel]] = None
    travelAsPassenger: Optional[List[Travel]] = None
    transports: Optional[List[Transport]] = None
