import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def parse_author_info(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        author_name = soup.find('h1', class_='Author_authorName__i4Wxb').text.strip()
        books_elements = soup.find_all('p', class_='ArtInfoTile_title__TCqN1')
        books = [book.text.strip() for book in books_elements]
        author_data = {
            'author_name': author_name,
            'books': books
        }

        json_data = json.dumps(author_data, ensure_ascii=False)
        return json_data
