from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Order_Default(SQLModel):
    number: int
class Order(Order_Default, table = True):
    route_id: Optional[int] = Field(default=None, foreign_key="route.id", primary_key=True)
    place_id: Optional[int] = Field(default=None, foreign_key="place.id", primary_key=True)

class Place_Default(SQLModel):
    name: str
    adress: str
    info: str
class Place(Place_Default, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routs: list['Route'] = Relationship(back_populates="places", link_model=Order)
    #level: Optional[int] = Field(default=None)


class Route_Default(SQLModel):
    name: str
    descryption:str

class Route(Route_Default, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    places: list['Place'] = Relationship(back_populates="routs", link_model=Order)
    journeys: list['Journey'] = Relationship(back_populates='route')

class Travel_Default(SQLModel):
    descryption: str

class Travel(Travel_Default, table = True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    journey_id: Optional[int] = Field(default=None, foreign_key="journey.id", primary_key=True)

class Journey_Default(SQLModel):
    name: str
    descryption: str

class Journey_Redact(Journey_Default):
    route_id: int = Field(default=None, nullable=True, foreign_key="route.id")

class Journey(Journey_Default, table = True):
    id: Optional[int] = Field(primary_key=True)
    route_id: int = Field(default=None, nullable=True, foreign_key="route.id")
    route: Optional[Route] = Relationship(back_populates="journeys")

    user_id: int = Field(default=None, foreign_key="user.id")
    user_owner: Optional['User'] = Relationship(back_populates="user_journeys")

    users: list['User'] = Relationship(back_populates="journeys", link_model=Travel)

class User_Default(SQLModel):
    username: str = Field(index=True)
    password: str
    email: str

class User_Submodel(User_Default):
    user_journeys: Optional[list['Journey']] = None

class User(User_Default, table=True):
    id: int = Field(default=None,primary_key=True)
    user_journeys: list['Journey'] = Relationship(back_populates='user_owner')
    journeys: list['Journey'] = Relationship(back_populates="users", link_model=Travel)




