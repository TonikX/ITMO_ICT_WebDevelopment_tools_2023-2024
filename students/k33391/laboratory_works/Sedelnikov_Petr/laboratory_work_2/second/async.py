import re

import aiohttp
import asyncio
import sqlite3
from bs4 import BeautifulSoup
import time


async def parse_litres(cursor, conn, session, category, params):
    async with session.get(f"https://www.litres.ru/{category}", params=params) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        books = soup.find_all('div', class_="ArtsGrid_artWrapper__LXa0O")
        count = 0
        for book in books:
            try:
                title = book.find('p', class_='ArtInfo_title__h_5Ay').get_text()
                author = book.find('a', class_='ArtInfo_author__0W3GJ').get_text()
                add_book(cursor, title, author)
                count += 1
            except Exception as e:
                pass
        print(f"Litres: {count}")
    commit(conn)


async def parse_bookvoed(cursor, conn, session, category, params):
    async with session.get(f"https://www.bookvoed.ru/{category}", params=params) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        books = soup.find_all('div', class_="product-card")
        count = 0
        for book in books:
            try:
                title = book.find('a', class_='product-description__link').get_text()
                author = book.find('a', class_='ui-comma-separated-links__author').get_text()
                add_book(cursor, title, author)
                count += 1
            except Exception as e:
                pass
        print(f"Bookvoed: {count}")
    commit(conn)


def get_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    author TEXT
                )
            ''')
    conn.commit()
    return conn, cursor


def add_book(cursor, title, author):
    cursor.execute('INSERT INTO books (name, author) VALUES (?, ?)', (title, author))


def commit(conn):
    conn.commit()


async def main():
    conn, cursor = get_db()
    tasks = []
    async with aiohttp.ClientSession() as session:
        task = asyncio.create_task(parse_litres(cursor, conn, session, 'genre/biznes-5003', {'art_types': 'text_book'}))
        tasks.append(task)
        task = asyncio.create_task(parse_bookvoed(cursor, conn, session, 'catalog/business-1671', {}))
        tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Async")
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
