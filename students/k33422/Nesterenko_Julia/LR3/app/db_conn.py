from sqlmodel import Session, create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from .models.transition_models import TransitionDefault, Transition
from .models.stay_models import StayDefault, Stay

import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DB_ADMIN')


engine = create_engine(db_url, echo=False)
session = Session(engine)


def save_stays(data):
    for d in data:
        statement = select(Stay).where(Stay.location == d[0],
                                       Stay.address == d[1],
                                       Stay.accomodation == d[2])          
        existing = session.exec(statement).all()
        if not existing:
            stay = StayDefault(location = d[0],
                               address = d[1],
                               accomodation = d[2])
            stay = Stay.model_validate(stay)
            session.add(stay)
            session.commit()
            session.refresh(stay)
    session.close()
    print(f"Saved {len(data)} items into the STAY database")
    

def save_transitions(data):
    for d in data:
        statement = select(Transition).where(Transition.location_from == d[0],
                                             Transition.location_to == d[1],
                                             Transition.transport == d[2])             
        existing = session.exec(statement).all()
        if not existing:
            transition = TransitionDefault(location_from = d[0],
                                        location_to = d[1],
                                        transport = d[2])
            transition = Transition.model_validate(transition)
            session.add(transition)
            session.commit()
            session.refresh(transition)
    session.close()
    print(f"Saved {len(data)} items into the TRANSITION database")