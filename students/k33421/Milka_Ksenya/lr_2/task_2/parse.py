import datetime

import aiohttp
import requests
from bs4 import BeautifulSoup

url = "https://freelance.habr.com/tasks"


async def async_get_content(page: int) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url + f"?page={page}") as response:
            return await response.text()


def get_content(page: int) -> str:
    return requests.get(url + f"?page={page}").text


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
