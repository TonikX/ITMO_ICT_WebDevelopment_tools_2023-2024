import os
from datetime import time

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()
db_url = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(db_url, echo=True)


def init_db():
    for i in range(10):
        try:
            SQLModel.metadata.create_all(engine)
            break
        except OperationalError as e:
            print(f"DB connection failed. Retrying in 3s... ({i + 1}/10)")
            time.sleep(3)


def get_session():
    with Session(engine) as session:
        yield session
