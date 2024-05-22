import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup

from db import WebPage, save_web_page
from util import bootstrap_environment, get_function_execution_time_sec_async
from shared import URLS


async def parse_and_save(client_session: aiohttp.ClientSession, url: str):
    logger = logging.getLogger()
    async with client_session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, 'html.parser')
        title = parsed_html.title.get_text()
        page = WebPage(title=title)
        try:
            page = save_web_page(page)
            logger.info('Web page saved. Generated id is %s', page.id)
        except Exception as e:
            logger.error('Failed to save web page')
            logger.exception(e)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in URLS]
        await asyncio.gather(*tasks)


async def wrapper():
    logger = logging.getLogger("Main")
    time_sec, *_ = await get_function_execution_time_sec_async(main)
    logger.info(f"Затраченное время - {time_sec:.3f} сек")


if __name__ == "__main__":
    bootstrap_environment()
    asyncio.run(wrapper())
