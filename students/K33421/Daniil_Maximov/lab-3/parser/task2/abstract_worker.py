import math
import re
from typing import Callable, Any

import httpx
from bs4 import BeautifulSoup

from task2.db import Session, Article


class AbstractWorker:
    _n_tasks: int

    _urls: list

    def __init__(self, n_tasks: int, urls: list):
        self._n_tasks = n_tasks
        self._urls = urls

    def run(self):
        raise NotImplementedError()

    @staticmethod
    def _sync_process_urls(urls: list[str]) -> None:
        for url in urls:
            html_content = AbstractWorker._sync_load_html_content_from_url(url)
            title = AbstractWorker._get_data_from_text_content(html_content)
            AbstractWorker._sync_save_to_db(title)

    @staticmethod
    def _sync_load_html_content_from_url(url: str) -> str:
        response = httpx.get(url)
        return response.text

    @staticmethod
    def _get_data_from_text_content(html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string.replace(' / Хабр', '')
        return title

    @staticmethod
    def _sync_save_to_db(title: str) -> None:
        session = Session()
        article = Article(title=title)
        session.add(article)
        print(f'Добавлена статья: {title}')
        session.commit()
        session.close()

    def _aggregate_tasks_for_range(self, create_task: Callable[[list[str]], Any]) -> list:
        chunk_size = math.ceil(len(self._urls) / self._n_tasks)
        tasks = []

        for i in range(self._n_tasks):
            task_start = i * chunk_size
            task_end = min((i + 1) * chunk_size, len(self._urls))
            task = create_task(self._urls[task_start:task_end])
            tasks.append(task)

            if task_end == len(self._urls):
                break

        return tasks
