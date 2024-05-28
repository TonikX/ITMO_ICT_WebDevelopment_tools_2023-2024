from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv, find_dotenv
"""import os
os.environ['POSTGRES_USER'] = "postgres"
os.environ['POSTGRES_PASSWORD'] = "123"
os.environ['POSTGRES_DB'] = "TimeManager"""


db_url = 'postgresql://postgres:123@db:5432/TimeManager'
# db_url = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@localhost:5432/{os.getenv("POSTGRES_DB")}"

engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# template is postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]