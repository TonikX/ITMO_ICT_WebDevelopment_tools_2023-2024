import asyncio
import time

import httpx

from db import AsyncSession
from enums import ParseMethod
from models import Title


async def parse_and_save(url: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    title = response.text.split("<title>")[1].split("</title>")[0].strip()
    title_model = Title(parse_method=ParseMethod.ASYNCIO, url=url, title=title)

    session = AsyncSession()
    session.add(title_model)
    await session.commit()


async def start_parsing() -> None:
    start_time = time.time()

    urls = [
        "https://student.itmo.ru/ru/repeat_interim_exams/",
        "https://student.itmo.ru/ru/expulsion_student_initiative/",
        "https://student.itmo.ru/ru/transfer/",
    ]

    await asyncio.gather(*(parse_and_save(url) for url in urls))

    print(f"Время: {time.time() - start_time}")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(start_parsing())