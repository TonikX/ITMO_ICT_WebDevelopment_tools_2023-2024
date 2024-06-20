from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
#db_url = 'postgresql://postgres:Scalapendra1219212712192127@localhost:5433/book_database'
load_dotenv()
db_url = os.getenv('DB_URL')

engine = create_engine(db_url, echo=True)
session = Session(bind=engine)
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session