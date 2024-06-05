from sqlmodel import SQLModel, Session, create_engine
from dotenv import dotenv_values
from pathlib import Path
from contextlib import contextmanager

env_path = Path(__file__).parent / '.env'
config = dotenv_values(env_path)
db_url = config['DB_ADMIN']
engine = create_engine(db_url)


def init_db():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session_func() -> Session:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_session_depends() -> Session:
    with Session(engine) as session:
        yield session
