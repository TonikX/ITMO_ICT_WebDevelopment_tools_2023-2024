import asyncio
import aiohttp
from bs4 import BeautifulSoup
import asyncpg
import time
import sys
import random


sys.stdout.reconfigure(encoding='utf-8')


async def parse_and_save(url, user_id):
    conditions = ['very good', 'good', 'normal', 'a bit damaged', 'old', 'perfect', 'brilliant', 'poor']
    start_time = time.time()
    books = []
    async with aiohttp.ClientSession() as session:
        conn = await asyncpg.connect('postgresql://mikalicce:qwerty@db:5432/book_crossing')
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            for book in soup.find_all('a', href=lambda href: href and '/book/oz' in href):
                title = book.text.strip().split('\n')[0]
                title = title.split('   ')[0]
                if title != '':
                    author = book.find_next('small').text.strip()
                    description = book.find_next('p').text.strip()
                    description = description.split('...')[0].strip()
                    description = description.replace('\t', '').replace('\n', '').replace('  ', '')
                    description = ' '.join(description.split())

                    random_condition = random.choice(conditions)

                    book_data = {
                        'title': title,
                        'author': author,
                        'description': description,
                        'condition': random_condition
                    }
                    books.append(book_data)
                    
                    await conn.execute("INSERT INTO book (title, author, description, condition, user_id) VALUES ($1, $2, $3, $4, $5)", title, author, description, random_condition, user_id)
            await conn.close()

    return {'books': books}