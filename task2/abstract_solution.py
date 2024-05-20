import math
import re
import httpx
from bs4 import BeautifulSoup

from task2.entities import Session, Article


class AbstractSolution:
    def __init__(self, n_tasks, urls):
        self._n_tasks = n_tasks
        self._urls = urls

    def run(self):
        raise NotImplementedError()

    @staticmethod
    def _sync_process_urls(urls):
        for url in urls:
            html_content = AbstractSolution._sync_load_html_content_from_url(url)
            title = AbstractSolution._sync_get_data_from_text_content(html_content)
            AbstractSolution._sync_save_to_db(url, title)

    @staticmethod
    def _sync_load_html_content_from_url(url):
        response = httpx.get(url)
        return response.text

    @staticmethod
    def _sync_get_data_from_text_content(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find(id='firstHeading')
        return title.text

    @staticmethod
    def _sync_save_to_db(url, title):
        session = Session()

        article = Article(url=url, title=title)
        session.add(article)

        print(f'Статья сохранена: {article}')

        session.commit()

        session.close()

    def _aggregate_tasks_for_range(self, create_task):
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
