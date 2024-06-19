import os
import aiohttp
import asyncio
import asyncpg
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv

load_dotenv()

# асинхронная функция для парсинга и сохранения данных
async def parse_and_save(url):
    # создаем асинхронную сессию для HTTP-запросов
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text

        # подключаемся к базе данных и выполняем вставку данных
        conn = await asyncpg.connect('postgresql://postgres:Bakugan102!@localhost:5432/web_data')
        try:
            await conn.execute(
                "INSERT INTO site (url, title) VALUES ($1, $2)",
                url, title
            )
        finally:
            await conn.close()

# главная асинхронная функция для запуска парсинга в параллельных задачах
async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = [
        'https://career.habr.com/vacancies?s%5B%5D=2&s%5B%5D=3&s%5B%5D=82&s%5B%5D=4&s%5B%5D=5&s%5B%5D=72&s%5B%5D=1&s%5B%5D=75&s%5B%5D=6&s%5B%5D=77&s%5B%5D=7&s%5B%5D=83&s%5B%5D=84&s%5B%5D=8&s%5B%5D=85&s%5B%5D=73&s%5B%5D=9&s%5B%5D=86&s%5B%5D=106&type=all',
        'https://career.habr.com/vacancies?s[]=2&s[]=3&s[]=82&s[]=4&s[]=5&s[]=72&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=84&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&s[]=106&sort=salary_desc&type=all',
        'https://career.habr.com/vacancies?s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true',
        'https://career.habr.com/vacancies?locations[]=c_699&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true'
    ]

    start_time = time.time()
    asyncio.run(main(urls))  # запускаем главную асинхронную функцию
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"async: {execution_time}")  # выводим время выполнения