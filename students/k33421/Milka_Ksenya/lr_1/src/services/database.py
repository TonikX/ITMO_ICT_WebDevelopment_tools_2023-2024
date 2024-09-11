from sqlalchemy.ext.asyncio import create_async_engine

from .. import config

engine = create_async_engine(
    config.database.dsn,
    echo=False,
)
