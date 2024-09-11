import datetime

import aiohttp
from bs4 import BeautifulSoup
from sqlmodel.ext.asyncio.session import AsyncSession

from .. import models
from ..services.database import engine

url = "https://freelance.habr.com/tasks"


async def async_get_content(page: int) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url + f"?page={page}") as response:
            return await response.text()


def parse_data(content: str) -> list[list]:
    soup = BeautifulSoup(content, 'html.parser')
    now = datetime.datetime.now()

    data_list = []
    for task_item in soup.select(".content-list__item"):
        title = task_item.select_one(".task__title a").get_text(strip=True)
        published_at = task_item.select_one(".params__published-at span").get_text(strip=True)

        tags = [tag.get_text(strip=True) for tag in task_item.select(".task__tags .tags__item_link")]
        tags_str = ", ".join(tags)

        description = f"{title}, {published_at}, Теги: {tags_str}"
        data_list.append([title, description, False, now])

    return data_list


async def upload_new_projects(page: int) -> int:
    async with AsyncSession(engine) as session:
        content = await async_get_content(page)
        data_list = parse_data(content)
        for title, description, is_active, start_date in data_list:
            project = models.Project(title=title, description=description, is_active=is_active, start_date=start_date)
            session.add(project)
        await session.commit()

    return len(data_list)
