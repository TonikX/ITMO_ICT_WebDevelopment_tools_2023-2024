import asyncio

import aiohttp
import httpx

from task2.db import AsyncSession, Article
from task2.abstract_worker import AbstractWorker


class AsyncWorker(AbstractWorker):
    def run(self) -> None:
        asyncio.run(self._run())

    async def _run(self) -> None:
        tasks = self._aggregate_tasks_for_range(self._async_process_urls)
        await asyncio.gather(*tasks)

    @staticmethod
    async def _async_process_urls(urls: list[str]) -> None:
        tasks = [AsyncWorker._async_process_single_url(url) for url in urls]
        await asyncio.gather(*tasks)

    @staticmethod
    async def _async_process_single_url(url: str) -> None:
        html_content = await AsyncWorker._async_load_html_content_from_url(url)
        title = AbstractWorker._get_data_from_text_content(html_content)
        await AsyncWorker._async_save_to_db(title)

    @staticmethod
    async def _async_save_to_db(title) -> None:
        async with AsyncSession() as session:
            async with session.begin():
                article = Article(title=title)
                session.add(article)
                print(f'Добавлена статья: {title}')
                await session.commit()

    @staticmethod
    async def _async_load_html_content_from_url(url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
