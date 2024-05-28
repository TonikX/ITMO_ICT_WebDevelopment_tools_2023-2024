from sqlmodel import SQLModel, Session, create_engine, Field
from decouple import config
from typing import Optional
from datetime import datetime, date

conn_str=config("DB_URL")
engine=create_engine(conn_str, echo=True)


# Trip models
class TripDefault(SQLModel):
    title: str
    date_start: date
    date_end: date
    estimated_cost: float
    trip_status: str
    other_details: Optional[str] = ""

class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_sesson():
    with Session(engine) as session:
        yield session

def create_trip(trip: TripDefault):
    with Session(engine) as session:
        trip = Trip.model_validate(trip)
        session.add(trip)
        session.commit()
        session.refresh(trip)
        return trip