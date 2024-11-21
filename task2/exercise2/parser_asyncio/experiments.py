from db_connection import get_session_context, engine_dispose
from sqlalchemy import select
import asyncio
import models
from elapsed_logging import logger
from contextlib import asynccontextmanager
from typing import AsyncGenerator

async def main():
    async with get_session_context() as session:
        query = select(models.Task)
        results = await session.exec(query)
        print(results.first())
    await engine_dispose()



if __name__ == "__main__":
    asyncio.run(main())
