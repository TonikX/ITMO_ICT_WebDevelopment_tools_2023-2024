from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from typing import AsyncIterator

env_path = Path(__file__).parent.parent / '.env'
config = dotenv_values(env_path)
db_url = config['DB_ADMIN_ASYNC']

async_engine = create_async_engine(
    db_url,
    future=True
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def get_session_context() -> AsyncIterator[AsyncSession]:
    # для использования в асинхронном контекстном менеджере
    session_maker = async_sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()


async def get_session_depends() -> AsyncIterator[AsyncSession]:
    # Сессия для использования в depends в fastAPI
    async_session = async_sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        

async def engine_dispose():
    # Разорвать соединение с БД
    await async_engine.dispose()