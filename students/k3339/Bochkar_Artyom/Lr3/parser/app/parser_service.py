import asyncio
import aiohttp
import asyncpg
import time
import random
import logging
import os

from datetime import datetime 
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv

from app.models import BookBase

# Настройка логирования
logger = logging.getLogger(__name__)

load_dotenv()

DB_ADMIN = os.getenv("DB_ADMIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_ADMIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Не все переменные окружения для БД найдены в .env файле")

DATABASE_URL = f"postgresql://{DB_ADMIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Глобальная переменная для пула соединений с БД
db_pool = None

async def init_db_pool():
    """Инициализация пула соединений с PostgreSQL"""
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            user=DB_ADMIN,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=int(DB_PORT),
            min_size=1,
            max_size=10
        )
        logger.info("Пул соединений с БД инициализирован")

async def close_db_pool():
    """Закрытие пула соединений"""
    global db_pool
    if db_pool:
        await db_pool.close()
        db_pool = None
        logger.info("Пул соединений с БД закрыт")

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
        return 0
        
    try:
        count = 0
        async with db_pool.acquire() as connection:
            for book_data in books:
                # Проверяем, существует ли книга уже в БД
                exists = await connection.fetchval(
                    "SELECT COUNT(*) FROM book WHERE title = $1 AND author = $2",
                    book_data.title, book_data.author
                )
                
                if not exists:
                    await connection.execute(
                        """
                        INSERT INTO book (title, author, description, owner_id, created_at)
                        VALUES ($1, $2, $3, $4, $5)
                        """,
                        book_data.title,
                        book_data.author,
                        book_data.description,
                        1,
                        datetime.utcnow()
                    )
                    count += 1
        
        logger.debug(f"Сохранено {count} новых книг в БД")
        return count
    except Exception as e:
        logger.error(f"Ошибка при сохранении книг: {e}")
        return 0

async def parse_and_save_books(url: str) -> int:
    """
    Основная функция для парсинга и сохранения книг
    Возвращает количество сохраненных книг
    """
    # Инициализируем пул соединений, если еще не инициализирован
    await init_db_pool()
    
    # Создаем HTTP сессию
    session = await create_session()
    
    try:
        logger.info(f"Начало парсинга: {url}")
        start_time = time.time()
        
        # Парсим книги
        books = await parse_books(session, url)
        
        if not books:
            logger.warning(f"Не удалось получить книги с {url}")
            return 0
        
        # Сохраняем книги в БД
        books_saved = await save_books_async(books)
        
        processing_time = time.time() - start_time
        logger.info(f"Обработано {len(books)} книг, сохранено {books_saved} новых книг с {url} за {processing_time:.2f} сек")
        
        return books_saved
        
    except Exception as e:
        logger.error(f"Ошибка при обработке URL {url}: {e}")
        raise
    finally:
        # Закрываем HTTP сессию
        await session.close()

async def cleanup():
    """Функция для очистки ресурсов при завершении приложения"""
    await close_db_pool()