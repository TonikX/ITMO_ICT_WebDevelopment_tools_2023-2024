from sqlmodel import SQLModel, Session, create_engine, Field
from src.settings.config import config
from src.models import Project


engine = create_engine(config.db_uri, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
    # Project.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
