from book_parser import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import sys
import time

sys.path.insert(0, "C:/Users/nic03/Uni/ITMO_ICT_WebDevelopment_tools_2023-2024/")

import warnings
from sqlalchemy import exc as sa_exc
import random
import aiohttp
import asyncio
from the_lab.base_models import BookBase
from the_lab.models import Book

import nest_asyncio

nest_asyncio.apply()

DB_URL = "postgresql+asyncpg://postgres:M1m1m1m1@localhost/library"
async_engine = create_async_engine(DB_URL, echo=False)
async_SessionFactory = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
warnings.filterwarnings("ignore", category=sa_exc.SAWarning)


async def fetch_book_details(
    book_id, session, api_key="AIzaSyAroYMo_JrN4UAdptepmm3DMp1ubMb0YEo"
):
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_id}&key={api_key}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if "items" in data and len(data["items"]) > 0:
                random_book = data["items"][0]["volumeInfo"]
                publication_year = random_book.get("publishedDate", "")[:4]
                try:
                    publication_year = int(publication_year)
                except ValueError:
                    publication_year = 2000
                return {
                    "title": random_book.get("title", "Нет названия"),
                    "author": ", ".join(random_book.get("authors", ["Нет автора"])),
                    "publication_year": publication_year,
                    "description": random_book.get("description", "Нет описания"),
                    "available": True,
                }
    return None


async def save_to_db(book_data, session_maker):
    async with session_maker() as session:
        async with session.begin():
            for book in book_data:
                publication_year = int(book["publication_year"])
                book_entry = Book(
                    name=book["title"],
                    author=book["author"],
                    publication_year=publication_year,
                    description=book["description"],
                    available=book["available"],
                )
                session.add(book_entry)


async def parse_and_save_async(book_id, http_session, db_session):
    book_data = await fetch_book_details(book_id, http_session)
    if book_data:
        await save_to_db([book_data], async_SessionFactory)
        print(f"Saved: {book_data['title']}")


async def async_version(book_ids):
    async with aiohttp.ClientSession() as http_session:
        async with async_SessionFactory() as db_session:
            tasks = [
                parse_and_save_async(book_id, http_session, db_session)
                for book_id in book_ids
            ]
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = fetch_random_book_ids(20)
    start_time = time.time()
    asyncio.run(async_version(urls))
    print(f"Multiprocessing version took {time.time() - start_time}")
