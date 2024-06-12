import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные окружения из .env

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/personal_finance_web_lab')


async def parse_and_save(url, session, database):
    async with session.get(url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')

        billionaires = soup.find_all("figcaption", class_="EXdHT")

        for billionaire in billionaires:
            name_tag = billionaire.find("h2", class_="jYzxi")
            balance_tag = billionaire.find("p", class_="ywx5e Q0w8z")

            if name_tag and balance_tag:
                name = name_tag.text.strip().split(" ", 1)[-1]
                balance_text = balance_tag.find("b", string=re.compile(r"Состояние:\s*"))

                if balance_text:
                    balance = balance_text.next_sibling.strip()
                else:
                    balance = balance_tag.find("b", string=re.compile(r"Доход:\с*")).next_sibling.strip()

                query = 'INSERT INTO finance (url, name, balance) VALUES (:url, :name, :balance)'
                values = {"url": url, "name": name, "balance": balance}
                await database.execute(query=query, values=values)


async def worker(urls, database):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(url, session, database) for url in urls]
        await asyncio.gather(*tasks)


async def main_start():
    urls = ["https://www.forbes.ru/milliardery/487053-10-bogatejsih-ludej-mira-2023-rejting-forbes",
            "https://www.forbes.ru/forbeslife/475277-samye-vysokooplacivaemye-tennisisty-mira-2022"]
    num_tasks = 1
    database = Database(DATABASE_URL)

    try:
        await database.connect()
        await database.execute('''
            CREATE TABLE IF NOT EXISTS finance (
                id SERIAL PRIMARY KEY,
                url TEXT,
                name TEXT,
                balance TEXT
            )
        ''')

        start_time = time.time()

        tasks = [asyncio.create_task(worker(urls[i::num_tasks], database)) for i in range(num_tasks)]
        await asyncio.gather(*tasks)

        await database.disconnect()
        end_time = time.time()
        return f"Parsed and saved data in {end_time - start_time} seconds"
    except Exception as e:
        return f"Unexpected error: {e}"


if __name__ == "__main__":
    asyncio.run(main_start())
