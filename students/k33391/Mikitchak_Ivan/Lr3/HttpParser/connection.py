from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from typing import AsyncGenerator

from dotenv import load_dotenv
import os


load_dotenv()
db_url = os.getenv("DB_URL")

async_engine = create_async_engine(url=db_url, echo=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session
