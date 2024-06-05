# Parse async

```
[Running] python -u "c:\Users\Alice\Desktop\shara\ITMO\Web 2 sem\local\Lab2\task2\parse_async.py"
Сохранен титул 'О рыцарях плаща и шпаги... - список литературы' из https://mybooklist.ru/list/483
Время парсинга: 0.40 секунд
Сохранен титул '100 книг, которые должен прочитать каждый - список литературы' из https://mybooklist.ru/list/1029
Время парсинга: 0.66 секунд
Сохранен титул 'Интеллектуальный бестселлер - список литературы' из https://mybooklist.ru/list/480
Время парсинга: 0.78 секунд
Сохранен титул 'Wish list - список литературы' из https://mybooklist.ru/list/1204
Время парсинга: 0.94 секунд
```


```
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import psycopg2
import re
import time
import sys
import random


sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://mybooklist.ru/list/1029',
    'https://mybooklist.ru/list/483',
    'https://mybooklist.ru/list/1204',
    'https://mybooklist.ru/list/480'
]

conn = psycopg2.connect(
    host="localhost",
    database="book_crossing",
    user="postgres",
    password="alison28",
    port=5433
)
c = conn.cursor()
```
Эта асинхронная функция выполняет следующие действия:  
- Открывает асинхронную сессию с помощью aiohttp.ClientSession().  
- Загружает содержимое веб-страницы по указанному url.  
- Использует BeautifulSoup для парсинга HTML-кода страницы.  
- Извлекает информацию о книгах (название, автор, описание, состояние) и сохраняет ее в базе данных PostgreSQL.  
- Записывает название страницы и время, затраченное на парсинг.
```
async def parse_and_save(url):
    conditions = ['very good', 'good', 'normal', 'a bit damaged', 'old', 'perfect', 'brilliant', 'poor']
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
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
                    
                    c.execute("INSERT INTO book (title, author, description, condition, user_id) VALUES (%s, %s, %s, %s, %s)", (title, author, description, random_condition, 2))
            title = soup.title.string

            conn.commit()
            print(f"Сохранен титул '{title}' из {url}")
            end_time = time.time()
            print(f"Время парсинга: {end_time - start_time:.2f} секунд")
```
Эта асинхронная функция использует asyncio.gather() для параллельного выполнения функции parse_and_save() для каждого из заданных URL-адресов.
```
async def main():
    await asyncio.gather(*[parse_and_save(url) for url in urls])
```
Этот блок кода запускает основную функцию main() в асинхронном режиме и закрывает подключение к базе данных.
```
if __name__ == '__main__':
    asyncio.run(main())
    conn.close()
```