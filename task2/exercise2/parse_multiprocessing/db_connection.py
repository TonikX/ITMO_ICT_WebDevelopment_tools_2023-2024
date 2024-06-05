from dotenv import dotenv_values
from contextlib import contextmanager
from pathlib import Path
from sqlmodel import Session, create_engine
from typing import Iterator


env_path = Path(__file__).parent.parent / '.env'
config = dotenv_values(env_path)
db_url = config['DB_ADMIN_SYNC']
engine = create_engine(db_url)


@contextmanager
def get_session_context() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# Depends зам позаботится о закрытии сессии, когда пишем генератор
def get_session_depends() -> Iterator[Session]:
    with Session(engine) as session:
        yield session