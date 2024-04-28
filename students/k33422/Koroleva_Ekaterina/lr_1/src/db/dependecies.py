from sqlalchemy.ext.asyncio import AsyncSession

from .helper import helper


async def scoped_session_dependency() -> AsyncSession:
    session = helper.get_scoped_session()
    yield session
    await session.close()
