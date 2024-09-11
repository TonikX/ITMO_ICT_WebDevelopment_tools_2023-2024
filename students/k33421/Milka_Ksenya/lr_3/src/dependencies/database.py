import typing as tp

from sqlmodel.ext.asyncio.session import AsyncSession

from ..services.database import engine


async def get_session() -> tp.AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
