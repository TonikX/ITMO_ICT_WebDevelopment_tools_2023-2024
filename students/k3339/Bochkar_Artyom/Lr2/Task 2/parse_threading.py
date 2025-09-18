# cd /Users/artboch/Documents/self-projects/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k3339/Bochkar_Artyom/Lr2
# source .venv/bin/activate
# python "Task 2/parse_threading.py"

import requests
from bs4 import BeautifulSoup
from sqlmodel import Session, create_engine, delete
import time
from models import *
from typing import List
import threading
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DATABASE_URL = "postgresql://postgres:superuser@localhost:5432/book_exchange_db"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

URLS = [
    "https://www.livelib.ru/author/103808/top-artur-konan-dojl",
    "https://www.livelib.ru/author/1781/top-agata-kristi",
    "https://www.livelib.ru/author/4389/top-sharlotta-bronte"
]

# Глобальная сессия с retry логикой
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Блокировка для синхронизации доступа к БД
db_lock = threading.Lock()


def clear_database():
    """Очистка базы данных перед началом работы"""
    with Session(engine) as session:
        session.exec(delete(Book))
        session.exec(delete(Profile))
        session.commit()
    print("База данных очищена")


def create_default_profile():
    """Создание профиля по умолчанию с id=1"""
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
        print("Создан профиль по умолчанию с id=1")


def parse_books(url: str) -> List[BookBase]:
    """Парсинг книг со страницы автора с улучшенной обработкой ошибок"""
    try:
        # Случайная задержка для избежания блокировки
        time.sleep(random.uniform(0.5, 1.5))
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = session.get(
            url, 
            headers=headers, 
            timeout=10,
            allow_redirects=True
        )
        response.raise_for_status()
        
        # Проверка на валидный HTML
        if not response.text.strip():
            print(f"Пустой ответ от {url}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        author_element = soup.find('div', class_='author-header__name')
        if not author_element:
            author_element = soup.find('h1', class_='author-header__title')
            
        author = author_element.text.strip() if author_element else "Неизвестный автор"

        books = []
        book_items = soup.find_all('div', class_='book-item__inner')
        
        if not book_items:
            print(f"Не найдено книг на странице: {url}")
            return []
            
        for book_item in book_items:
            try:
                title_element = book_item.find('a', class_='book-item__title')
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                
                description_element = book_item.find('p')
                if not description_element:
                    description_element = book_item.find('div', class_='book-item__annotation')
                    
                description = None
                if description_element:
                    description_text = description_element.text.strip()
                    if description_text:
                        sentences = description_text.split('.')
                        description = '.'.join(sentences[:3]) + '.' if len(sentences) > 3 else description_text

                books.append(BookBase(
                    title=title,
                    author=author,
                    description=description,
                ))
                
            except Exception as e:
                print(f"Ошибка при обработке книги: {e}")
                continue

        return books
        
    except requests.exceptions.Timeout:
        print(f"Таймаут при запросе к {url}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе к {url}: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при парсинге {url}: {e}")
        return []


def save_books(books: List[BookBase]):
    """Сохранение книг в БД с блокировкой"""
    if not books:
        return
        
    try:
        with db_lock:
            with Session(engine) as db_session:
                for book_data in books:
                    book = Book(**book_data.model_dump(), owner_id=1)
                    db_session.add(book)
                db_session.commit()
    except Exception as e:
        print(f"Ошибка при сохранении книг: {e}")


def parse_and_save(url: str):
    """Функция для потока: парсинг и сохранение"""
    print(f"Начало парсинга: {url}")
    start_time = time.time()
    
    books = parse_books(url)
    
    if books:
        save_books(books)
        print(f"Сохранено {len(books)} книг с {url} за {time.time() - start_time:.2f} сек")
    else:
        print(f"Не удалось получить книги с {url}")


def main():
    start_time = time.time()

    clear_database()
    create_default_profile()

    threads = []
    for url in URLS:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
        time.sleep(0.1)

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")


if __name__ == "__main__":
    main()