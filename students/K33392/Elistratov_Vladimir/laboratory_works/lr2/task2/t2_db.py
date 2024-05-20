from t2_City import City
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    session = Session(engine)
    return session



def add_city(city: City) -> City:
    session = get_session()
    try:
        #print(page)
        session.add(city)
        session.commit()
    finally:
        #print(" !!!\n")
        session.close()


if __name__ == "__main__":
    init_db()