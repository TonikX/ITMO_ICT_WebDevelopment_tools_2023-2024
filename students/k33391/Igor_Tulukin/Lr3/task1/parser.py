import aiohttp
from bs4 import BeautifulSoup
from db import save_to_db
from fastapi import HTTPException

async def parse_and_save(url: str):
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to retrieve the URL")
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.title.string if soup.title else 'No Title'
            save_to_db(url, title)
            return title
