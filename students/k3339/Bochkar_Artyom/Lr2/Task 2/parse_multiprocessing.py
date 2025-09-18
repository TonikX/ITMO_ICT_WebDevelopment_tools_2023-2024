# cd /Users/artboch/Documents/self-projects/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k3339/Bochkar_Artyom/Lr2
# source .venv/bin/activate
# python "Task 2/parse_multiprocessing.py"

import requests
from bs4 import BeautifulSoup
from sqlmodel import Session, create_engine, delete
import time
from models import *
from typing import List
import multiprocessing
from multiprocessing import Pool, Manager
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres:superuser@localhost:5432/book_exchange_db"
URLS = [
    "https://www.livelib.ru/author/103808/top-artur-konan-dojl",
    "https://www.livelib.ru/author/1781/top-agata-kristi",
    "https://www.livelib.ru/author/4389/top-sharlotta-bronte"
]

# Глобальная сессия с retry логикой (будет создаваться в каждом процессе)
def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def init_worker():
    """Инициализация worker'а - создание движка БД и сессии"""
    global engine, session
    engine = create_engine(DATABASE_URL)
    session = create_session()


def clear_database():
    """Очистка базы данных перед началом работы"""
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        session.exec(delete(Book))
        session.exec(delete(Profile))
        session.commit()
    logger.info("База данных очищена")


def create_default_profile():
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


def parse_books(url: str) -> List[BookBase]:
    """Парсинг книг со страницы автора"""
    try:
        # Случайная задержка для избежания блокировки
        time.sleep(random.uniform(0.5, 1.5))
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
        }
        
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
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
        
    except requests.exceptions.Timeout:
        logger.warning(f"Таймаут при запросе к {url}")
        return []
    except requests.exceptions.RequestException as e:
        logger.warning(f"Ошибка сети при запросе к {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при парсинге {url}: {e}")
        return []


def save_books(books: List[BookBase]):
    """Сохранение книг в БД"""
    if not books:
        return
        
    try:
        # Каждый процесс имеет свой собственный движок БД
        local_engine = create_engine(DATABASE_URL)
        with Session(local_engine) as db_session:
            for book_data in books:
                book = Book(**book_data.model_dump(), owner_id=1)
                db_session.add(book)
            db_session.commit()
        logger.debug(f"Сохранено {len(books)} книг в БД")
    except Exception as e:
        logger.error(f"Ошибка при сохранении книг: {e}")


def process_url(url: str):
    """Функция для обработки одного URL в процессе"""
    logger.info(f"Начало обработки: {url}")
    start_time = time.time()
    
    books = parse_books(url)
    
    if books:
        save_books(books)
        processing_time = time.time() - start_time
        logger.info(f"Обработано {len(books)} книг с {url} за {processing_time:.2f} сек")
        return len(books), processing_time
    else:
        logger.warning(f"Не удалось получить книги с {url}")
        return 0, time.time() - start_time


def main():
    start_time = time.time()

    # Очистка и создание профиля в основном процессе
    clear_database()
    create_default_profile()

    logger.info(f"Запуск multiprocessing с {len(URLS)} процессами")
    
    # Используем Pool с инициализацией worker'ов
    with Pool(processes=min(4, len(URLS)), initializer=init_worker) as pool:
        results = pool.map(process_url, URLS)
    
    # Анализ результатов
    total_books = sum(books for books, _ in results)
    total_time = time.time() - start_time
    
    logger.info(f"=== РЕЗУЛЬТАТЫ ===")
    logger.info(f"Всего обработано книг: {total_books}")
    logger.info(f"Общее время выполнения: {total_time:.2f} секунд")
    
    for i, (url, (books, time_taken)) in enumerate(zip(URLS, results)):
        logger.info(f"URL {i+1}: {books} книг за {time_taken:.2f} сек")


if __name__ == "__main__":
    # Для Windows обязательно использовать freeze_support
    multiprocessing.freeze_support()
    
    # Установка стартового метода для лучшей совместимости
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        pass
    
    main()