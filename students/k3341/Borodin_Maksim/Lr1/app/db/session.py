from sqlmodel import Session, create_engine

from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=settings.db_echo)


def get_session():
    with Session(engine) as session:
        yield session
