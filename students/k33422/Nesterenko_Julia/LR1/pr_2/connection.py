from sqlmodel import SQLModel, Session, create_engine
from creds import USERNAME, PASSWORD

db_url = f'postgresql://{USERNAME}:{PASSWORD}@localhost:5432/pr_1'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session