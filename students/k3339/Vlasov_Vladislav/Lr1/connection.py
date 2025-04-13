import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv
from sqlmodel import SQLModel

load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_async_engine(db_url, echo=True)


async def init_db():
    async with engine.begin() as conn:
        # Создание всех таблиц в базе данных
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session