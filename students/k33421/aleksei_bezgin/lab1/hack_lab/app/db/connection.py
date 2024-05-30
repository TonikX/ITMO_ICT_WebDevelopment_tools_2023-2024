from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings


DATABASE_DSN = (
    f"postgresql+psycopg://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)


engine = create_engine(DATABASE_DSN, echo=True)
async_engine = create_async_engine(DATABASE_DSN)