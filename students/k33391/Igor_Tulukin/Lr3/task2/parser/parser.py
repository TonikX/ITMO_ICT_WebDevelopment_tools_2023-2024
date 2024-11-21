import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DB_ADMIN")

db_url = f"{db_url}"


def save_to_db(url, title):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO page (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()
    cursor.close()
    conn.close()

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
