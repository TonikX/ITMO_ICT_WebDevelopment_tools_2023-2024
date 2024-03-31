from sqlmodel import create_engine, SQLModel
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
