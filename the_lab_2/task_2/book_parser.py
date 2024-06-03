from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import sys
import warnings
from sqlalchemy import exc as sa_exc


sys.path.insert(0, "C:/Users/nic03/Uni/ITMO_ICT_WebDevelopment_tools_2023-2024/")
from the_lab.base_models import BookBase
from the_lab.models import Book

import requests
import random

DB_URL = "postgresql://postgres:M1m1m1m1@localhost/library"
engine = create_engine(DB_URL, echo=False)
SessionFactory = sessionmaker(bind=engine)
session = scoped_session(SessionFactory)
warnings.filterwarnings("ignore", category=sa_exc.SAWarning)


def fetch_random_book_ids(num_books=20):
    return [str(random.randint(1, 60000)) for _ in range(num_books)]


def get_book_details(book_id, api_key="AIzaSyAroYMo_JrN4UAdptepmm3DMp1ubMb0YEo"):
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_id}&key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            random_book = data["items"][0]["volumeInfo"]
            return {
                "title": random_book.get("title", "Нет названия"),
                "author": ", ".join(random_book.get("authors", "Нет автора")),
                "publication_year": random_book.get("publishedDate", 2000)[:4],
                "description": random_book.get("description", "Нет описания"),
                "available": True,
            }
    return None


def save_to_db(book_data):
    for book in book_data:
        book_entry = Book(
            name=book["title"],
            author=book["author"],
            publication_year=book["publication_year"],
            description=book["description"],
            available=book["available"],
        )
        session.add(book_entry)
    session.commit()


async def fetch_book_details(
    book_id, session, api_key="AIzaSyAroYMo_JrN4UAdptepmm3DMp1ubMb0YEo"
):
    url = f"https://www.googleapis.com/books/v1/volumes?q={book_id}&key={api_key}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if "items" in data and len(data["items"]) > 0:
                random_book = data["items"][0]["volumeInfo"]
                return {
                    "title": random_book.get("title", "Нет названия"),
                    "author": ", ".join(random_book.get("authors", ["Нет автора"])),
                    "publication_year": random_book.get(
                        "publishedDate", "Нет года издания"
                    )[:4],
                    "description": random_book.get("description", "Нет описания"),
                    "available": True,
                }
    return None


urls = fetch_random_book_ids(20)
