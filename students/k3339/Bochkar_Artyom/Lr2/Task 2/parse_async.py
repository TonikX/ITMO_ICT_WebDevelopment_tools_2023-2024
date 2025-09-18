# cd /Users/artboch/Documents/self-projects/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k3339/Bochkar_Artyom/Lr2
# source .venv/bin/activate
# python "Task 2/parse_async.py"

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from sqlmodel import Session, create_engine, delete
import time
from models import *
from typing import List
import random
import logging
import asyncpg
from contextlib import asynccontextmanager

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres:superuser@localhost:5432/book_exchange_db"
URLS = [
    "https://www.livelib.ru/author/103808/top-artur-konan-dojl",
    "https://www.livelib.ru/author/1781/top-agata-kristi",
    "https://www.livelib.ru/author/4389/top-sharlotta-bronte"
]

# Глобальная переменная для пула соединений с БД
db_pool = None

async def init_db_pool():
    """Инициализация пула соединений с PostgreSQL"""
    global db_pool
    db_pool = await asyncpg.create_pool(
        user='postgres',
        password='superuser',
        database='book_exchange_db',
        host='localhost',
        port=5432,
        min_size=1,
        max_size=10
    )
    logger.info("Пул соединений с БД инициализирован")

async def close_db_pool():
    """Закрытие пула соединений"""
    if db_pool:
        await db_pool.close()
        logger.info("Пул соединений с БД закрыт")

async def clear_database():
    """Очистка базы данных перед началом работы"""
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        session.exec(delete(Book))
        session.exec(delete(Profile))
        session.commit()
    logger.info("База данных очищена")

async def create_default_profile():
    """Создание профиля по умолчанию с id=1"""
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        default_profile = Profile(
            id=1,
            username="default_user",
            name="Default",
            surname="User",
            age=30,
            gender=Gender.MALE,
            address="Default address"
        )
        session.add(default_profile)
        session.commit()
    logger.info("Создан профиль по умолчанию с id=1")

async def create_session():
    """Создание асинхронной HTTP сессии"""
    timeout = aiohttp.ClientTimeout(total=30)
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
    session = aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }
    )
    return session

async def parse_books(session: aiohttp.ClientSession, url: str) -> List[BookBase]:
    """Асинхронный парсинг книг со страницы автора"""
    try:
        # Случайная задержка для избежания блокировки
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Более надежное извлечение автора
            author_element = soup.find('div', class_='author-header__name') or soup.find('h1', class_='author-header__title')
            author = author_element.text.strip() if author_element else "Неизвестный автор"

            books = []
            book_items = soup.find_all('div', class_='book-item__inner')
            
            for book_item in book_items:
                try:
                    title_element = book_item.find('a', class_='book-item__title')
                    if not title_element:
                        continue
                        
                    title = title_element.text.strip()
                    
                    description_element = book_item.find('p') or book_item.find('div', class_='book-item__annotation')
                    description = None
                    if description_element and description_element.text.strip():
                        desc_text = description_element.text.strip()
                        sentences = desc_text.split('.')
                        description = '.'.join(sentences[:3]) + '.' if len(sentences) > 3 else desc_text

                    books.append(BookBase(
                        title=title,
                        author=author,
                        description=description,
                    ))
                    
                except Exception as e:
                    logger.warning(f"Ошибка при обработке книги: {e}")
                    continue

            return books
            
    except asyncio.TimeoutError:
        logger.warning(f"Таймаут при запросе к {url}")
        return []
    except aiohttp.ClientError as e:
        logger.warning(f"Ошибка сети при запросе к {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при парсинге {url}: {e}")
        return []

async def save_books_async(books: List[BookBase]):
    """Асинхронное сохранение книг в БД с использованием asyncpg"""
    if not books:
        return
        
    try:
        async with db_pool.acquire() as connection:
            for book_data in books:
                # Используем raw SQL для асинхронной вставки
                await connection.execute(
                    """
                    INSERT INTO book (title, author, description, owner_id)
                    VALUES ($1, $2, $3, $4)
                    """,
                    book_data.title,
                    book_data.author,
                    book_data.description,
                    1
                )
        logger.debug(f"Сохранено {len(books)} книг в БД")
    except Exception as e:
        logger.error(f"Ошибка при сохранении книг: {e}")

async def process_url(session: aiohttp.ClientSession, url: str):
    """Асинхронная функция для обработки одного URL"""
    logger.info(f"Начало обработки: {url}")
    start_time = time.time()
    
    books = await parse_books(session, url)
    
    if books:
        await save_books_async(books)
        processing_time = time.time() - start_time
        logger.info(f"Обработано {len(books)} книг с {url} за {processing_time:.2f} сек")
        return len(books), processing_time
    else:
        logger.warning(f"Не удалось получить книги с {url}")
        return 0, time.time() - start_time

async def main():
    """Основная асинхронная функция"""
    start_time = time.time()

    # Инициализация пула соединений с БД
    await init_db_pool()

    # Очистка и создание профиля
    await clear_database()
    await create_default_profile()

    logger.info(f"Запуск async с {len(URLS)} задачами")
    
    # Создаем HTTP сессию
    session = await create_session()
    
    try:
        # Создаем задачи для каждого URL
        tasks = [process_url(session, url) for url in URLS]
        
        # Запускаем все задачи параллельно
        results = await asyncio.gather(*tasks)
        
        # Анализ результатов
        total_books = sum(books for books, _ in results)
        total_time = time.time() - start_time
        
        logger.info(f"=== РЕЗУЛЬТАТЫ ===")
        logger.info(f"Всего обработано книг: {total_books}")
        logger.info(f"Общее время выполнения: {total_time:.2f} секунд")
        
        for i, (url, (books, time_taken)) in enumerate(zip(URLS, results)):
            logger.info(f"URL {i+1}: {books} книг за {time_taken:.2f} сек")
            
    finally:
        # Закрываем сессию и пул соединений
        await session.close()
        await close_db_pool()

if __name__ == "__main__":
    # Запуск асинхронной программы
    asyncio.run(main())