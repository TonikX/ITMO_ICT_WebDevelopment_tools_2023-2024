from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.exc import SQLAlchemyError

from src.config import db_settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False
    ):
        self.url: str = url
        self.echo: bool = echo

        self.engine: AsyncEngine = create_async_engine(url=self.url, echo=self.echo)

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self):
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


helper: DatabaseHelper = DatabaseHelper(
    url=db_settings.get_dsn(),
    echo=db_settings.echo
)
