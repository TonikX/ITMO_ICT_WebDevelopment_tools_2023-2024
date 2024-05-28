from celery import Celery
import aiohttp
from bs4 import BeautifulSoup
import ssl
from database import commit_article
import asyncio
from celery_config import app

@app.task
def fetch_and_store_title(url: str):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async def fetch_title():
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return {'status': 'error', 'message': 'Error fetching the URL'}
                html = await response.text()
                parsed_html = BeautifulSoup(html, 'html.parser')
                title = parsed_html.title.string if parsed_html.title else 'No title found'
                commit_article(title)  
                return {'status': 'success', 'title': title}

    return asyncio.get_event_loop().run_until_complete(fetch_title())

