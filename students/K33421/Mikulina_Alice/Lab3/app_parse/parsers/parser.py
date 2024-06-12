import os
import sys
import random
import asyncio
import aiohttp
import asyncpg
from bs4 import BeautifulSoup
from celery import shared_task


CONDITIONS = ['very good', 'good', 'normal', 'a bit damaged', 'old', 'perfect', 'brilliant', 'poor']
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')

db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


@shared_task
def parse_and_save_task(url, user_id):
    loop = asyncio.new_event_loop()
    task = loop.create_task(parse_and_save(url, user_id))
    loop.run_until_complete(task)
    return task.result()


async def parse_and_save(url, user_id):
    books = []

    async with aiohttp.ClientSession() as session:
        conn = await asyncpg.connect(db_url)
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            for book in soup.find_all('a', href=lambda href: href and '/book/oz' in href):
                title = book.text.strip().split('\n')[0]
                title = title.split('   ')[0]
                if title == '':
                    continue
                author = book.find_next('small').text.strip()
                description = book.find_next('p').text.strip()
                description = description.split('...')[0].strip()
                description = description.replace('\t', '').replace('\n', '').replace('  ', '')
                description = ' '.join(description.split())

                random_condition = random.choice(CONDITIONS)

                book_data = {
                    'title': title,
                    'author': author,
                    'description': description,
                    'condition': random_condition
                }
                books.append(book_data)

                await conn.execute(
                    "INSERT INTO book (title, author, description, condition, user_id) VALUES ($1, $2, $3, $4, $5)",
                    title, author, description, random_condition, user_id
                )
            await conn.close()

    return {'books': books}
