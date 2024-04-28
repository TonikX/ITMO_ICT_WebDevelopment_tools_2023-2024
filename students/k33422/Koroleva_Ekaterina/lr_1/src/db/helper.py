from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from src.config import db_settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.url: str = url
        self.echo: bool = echo

        self.engine: AsyncEngine = create_async_engine(url=self.url, echo=self.echo)

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        return async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )


helper: DatabaseHelper = DatabaseHelper(
    url=db_settings.get_dsn(), echo=db_settings.echo
)
