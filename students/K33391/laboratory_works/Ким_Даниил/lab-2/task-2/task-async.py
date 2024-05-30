import re

import aiohttp
import asyncio
import sqlite3
from bs4 import BeautifulSoup
import time


async def parse_and_save(url, session, cursor, conn):
    async with session.get(url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')

        billionaires = soup.find_all("figcaption", class_="EXdHT")
        for billionaire in billionaires:
            name_tag = billionaire.find("h2", class_="jYzxi")
            balance_tag = billionaire.find("p", class_="ywx5e Q0w8z")

            if name_tag and balance_tag:
                name = name_tag.text.strip().split(" ", 1)[-1]  # Извлекаем имя без "№2"
                balance_text = balance_tag.find("b", string=re.compile(r"Состояние:\s*"))
                if balance_text:
                    balance = balance_text.next_sibling.strip()
                else:
                    balance = "Неизвестно"

                cursor.execute('INSERT INTO finance (url, name, balance) VALUES (?, ?, ?)', (url, name, balance))
        conn.commit()


async def worker(urls, cursor, conn):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, cursor, conn) for url in urls]
        await asyncio.gather(*tasks)


async def main():
    urls = ["https://www.forbes.ru/milliardery/487053-10-bogatejsih-ludej-mira-2023-rejting-forbes"]
    num_tasks = 1
    try:
        conn = sqlite3.connect('personal_finance.db')
        cursor = conn.cursor()

        # Создаем таблицу, если она еще не создана
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS finance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                name TEXT,
                balance TEXT
            )
        ''')
        conn.commit()

        start_time = time.time()

        tasks = []
        for i in range(num_tasks):
            task = asyncio.create_task(worker(urls[i::num_tasks], cursor, conn))
            tasks.append(task)

        await asyncio.gather(*tasks)

        conn.close()
        end_time = time.time()
        print(f"Parsed and saved data in {end_time - start_time} seconds")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())