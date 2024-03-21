from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lab.config import settings


database_config = settings.database

DATABASE_DSN = (
    f"postgresql+psycopg://{database_config.user}:{database_config.password}"
    f"@{database_config.host}:{database_config.port}/{database_config.name}"
)


engine = create_engine(DATABASE_DSN, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database_session() -> Session:
    session = SessionLocal()
    with session:
        yield session
        session.rollback()
        session.close()


DatabaseSession = Annotated[Session, Depends(get_database_session)]
