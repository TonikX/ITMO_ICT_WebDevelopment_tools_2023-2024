import aiohttp
import asyncio
from bs4 import BeautifulSoup
from time import time
from db.connection import get_session, init_categories, init_db
from db.models import Task, Category
from sqlmodel import select

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_and_save(url):
    async with aiohttp.ClientSession() as http_session:
        html = await fetch(http_session, url)
        soup = BeautifulSoup(html, 'html.parser')
        questions = soup.select(".s-post-summary")

        async for session in get_session():
            for q in questions:
                title_tag = q.select_one(".s-post-summary--content-title")
                desc_tag  = q.select_one(".s-post-summary--content-excerpt")
                title  = title_tag.text.strip() if title_tag else "Без названия"
                descr  = desc_tag.text.strip()  if desc_tag  else "Без описания"

                answers_block = q.select_one(".s-post-summary--stats-item")
                num_tag = answers_block.select_one(".s-post-summary--stats-item-number") if answers_block else None
                num = int(num_tag.text.strip()) if num_tag and num_tag.text.strip().isdigit() else 0

                category_name = "Answered" if num > 0 else "Unanswered"
                category = (await session.execute(select(Category).where(Category.name == category_name))).scalar_one_or_none()

                task = Task(title=title, description=descr, user_id=1, categories=[category])
                session.add(task)
                await session.commit()
                await session.refresh(task)

                print(f"[ASYNC] {title} → {category_name}")

            session.close()

async def main():
    pages = 20
    urls = [f"https://stackoverflow.com/questions?tab=newest&page={i}" for i in range(1, pages + 1)]
    await init_db()
    await init_categories()

    start = time()

    await asyncio.gather(*(parse_and_save(url) for url in urls))

    print(f"[ASYNC] Время выполнения: {time() - start:.2f} секунд")

if __name__ == "__main__":
    asyncio.run(main())

# [ASYNC] Время выполнения: 5.19 секунд