from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db.connection import engine


def get_database_session() -> Session:
    with Session(engine) as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_database_session)]