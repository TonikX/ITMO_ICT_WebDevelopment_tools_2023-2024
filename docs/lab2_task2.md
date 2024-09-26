!!! example "Задание"
    Напиcать программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных 
    с использованием подходов threading, multiprocessing и async.
    Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

=== "theading_parser"

    ``` py
    import threading
    import time
    
    import httpx
    
    
    from db import Session
    from enums import ParseMethod
    from models import Title
    
    
    def parse_and_save(url: str) -> None:
        with httpx.Client() as client:
            response = client.get(url)
    
        title = response.text.split("<title>")[1].split("</title>")[0].strip()
        title_model = Title(parse_method=ParseMethod.THREADING, url=url, title=title)
    
        with Session() as session:
            session.add(title_model)
            session.commit()
        print(f"{url} - {title}")
    
    def start_parsing() -> None:
        start_time = time.time()
    
        urls = [
            "https://student.itmo.ru/ru/repeat_interim_exams/",
            "https://student.itmo.ru/ru/expulsion_student_initiative/",
            "https://student.itmo.ru/ru/transfer/",
        ]
    
        threads = [threading.Thread(target=parse_and_save, args=(url,)) for url in urls]
    
        for thread in threads:
            thread.start()
    
        for thread in threads:
            thread.join()
    
        print(f"Время: {time.time() - start_time}")
    
    
    if __name__ == "__main__":
        start_parsing()

    ```
    Описание работы -  извлекаем содержимое тега из HTML ответа, создаем модель, с помощью threading создаем потоки 
    для каждого URL тем самым параллельно извлекая загаловки с веб страниц
    
=== "multiprocessing_parser"

    ``` py
    import multiprocessing
    import time
    
    import httpx
    
    from db import Session
    from enums import ParseMethod
    from models import Title
    
    
    def parse_and_save(url: str) -> None:
        with httpx.Client() as client:
            response = client.get(url)
    
        title = response.text.split("<title>")[1].split("</title>")[0].strip()
        title_model = Title(parse_method=ParseMethod.MULTIPROCESSING, url=url, title=title)
    
        with Session() as session:
            session.add(title_model)
            session.commit()
        print(f"{url} - {title}")
    
    def start_parsing() -> None:
        start_time = time.time()
    
        urls = [
            "https://student.itmo.ru/ru/repeat_interim_exams/",
            "https://student.itmo.ru/ru/expulsion_student_initiative/",
            "https://student.itmo.ru/ru/transfer/",
        ]
    
        with multiprocessing.Pool(processes=3) as pool:
            pool.map(parse_and_save, urls)
    
        print(f"Время: {time.time() - start_time}")
    
    
    if __name__ == "__main__":
        start_parsing()

    ```
    Описание работы - аналогично threadin парсеру, реализуем извлечение заголовков, но используя разделение на процессы
     с помощью multiprocessing

=== "asyncio_parser"

    ``` py
    import asyncio
    import time
    
    import httpx
    
    from db import AsyncSession
    from enums import ParseMethod
    from models import Title
    
    
    async def parse_and_save(url: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    
        title = response.text.split("<title>")[1].split("</title>")[0].strip()
        title_model = Title(parse_method=ParseMethod.ASYNCIO, url=url, title=title)
    
        session = AsyncSession()
        session.add(title_model)
        await session.commit()
        print(f"{url} - {title}")
    
    
    async def start_parsing() -> None:
        start_time = time.time()
    
        urls = [
            "https://student.itmo.ru/ru/repeat_interim_exams/",
            "https://student.itmo.ru/ru/expulsion_student_initiative/",
            "https://student.itmo.ru/ru/transfer/",
        ]
    
        await asyncio.gather(*(parse_and_save(url) for url in urls))
    
        print(f"Время: {time.time() - start_time}")
    
    
    if __name__ == "__main__":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(start_parsing())

    ```
    Описание работы - используем asyncio.gather чтобы парралельно запускать несколько задач и эффективно обрабатывать все URL

=== "models"

    ``` py
    import datetime

    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    
    from db import engine
    from enums import ParseMethod
    
    
    class Base(DeclarativeBase):
        pass
    
    
    class Title(Base):
        __tablename__ = "titles"
    
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        parse_method: Mapped[ParseMethod]
        url: Mapped[str]
        title: Mapped[str]
        created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    
    
    def create_db_and_tables() -> None:
        Base.metadata.create_all(engine)
    
    
    if __name__ == "__main__":
        create_db_and_tables()

    ```
    Описание работы -  определяем структуру базы данных и создаем таблицу для хранения спаршенных в будущем заголовков
    веб страниц

=== "enums"

    ``` py
    import enum
    
    
    class ParseMethod(enum.Enum):
        THREADING = "threading"
        MULTIPROCESSING = "multiprocessing"
        ASYNCIO = "asyncio"

    ```
    Описание работы -  также создаем модель таблицы в которой будем хранить спаршенные заголовки страниц

=== "База данных"

    ``` py
    import os
    from pathlib import Path
    
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.orm import sessionmaker
    
    load_dotenv()
    
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    
    # подключаем синхронное и асинхронное использование
    DATABASE_DSN = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    ASYNC_DATABASE_DSN = f"postgresql+psycopg_async://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    engine = create_engine(DATABASE_DSN)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    async_engine = create_async_engine(ASYNC_DATABASE_DSN)
    AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)
    ```
    Описание работы -  загружаем переменные окружения, определяем параметры подключения к бд, формируем строки подключения
     и создаем синхронные и асинхронные движки для базы данных

ВЫВОД

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/lab_2_console_pars.png) 
    спаршенные заголовки

Время
- threading - 1.73сек
- multiprocessing - 2.85сек
- async - 2.57сек

Cкромная задача для сравнения разных методов разделения работы, но на таком примере мы можем увидеть, что для маленького
обьема информации нет смысла использовать multiprocessing и при этом по очевидным причинам treading несколько быстрее
чем async
