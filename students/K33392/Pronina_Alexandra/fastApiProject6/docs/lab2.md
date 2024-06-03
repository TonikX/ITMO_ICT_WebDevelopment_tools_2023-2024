### Задание 1:
Измеренное время выполнения для async, process и thread выглядит следующим образом:

Async: 0.0474 секунды
Process: 0.05213 секунды
Thread: 0.0492 секунды

Возможные причины для таких результатов:

1. GIL (Global Interpreter Lock): Python использует GIL, который предотвращает одновременное выполнение нескольких потоков Python кода в одном процессе. Это может снизить эффективность многопоточных подходов в некоторых случаях. Однако асинхронный подход не страдает от этого, так как он не использует потоки Python.

2. Создание процессов: Подход с использованием multiprocessing (process) создает отдельные процессы, что требует больше времени и ресурсов.

3. Управление ресурсами: В многопоточном подходе (thread) создается несколько потоков, но они разделяют один и тот же ресурс процесса, что может повлечь за собой меньшие накладные расходы по сравнению с созданием отдельных процессов.

### Задание 2:

Далее будет 3 скрипта, которые представляют собой скрипты для парсинга информации о путешествиях с различных сайтов и сохранения данных в базу данных. В качестве примеров используются четыре разных URL-адреса, каждый из которых содержит информацию о различных туристических мероприятиях.

async.py:
    
    import asyncio
    import aiohttp
    from bs4 import BeautifulSoup
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
    from sqlalchemy.orm import sessionmaker
    from database import Trip, SessionLocal
    import time
    from datetime import datetime
    import re
    import json
    
    
    async def parse_and_save(url):
        start_time = time.time()
    
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
    
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string
    
        departure_location_element = soup.find("div", class_="tags")
        departure_location = departure_location_element.find("a",
                                                             class_="tag has-icon-location").text.strip() if departure_location_element else "Unknown"
    
        date_option = soup.select_one("option[selected='selected']")
        if date_option:
            date_text = date_option.text.strip()
            if " — " in date_text and " " in date_text:
                start_day, end_month_year = date_text.split(" — ", maxsplit=1)
                end_day, month_year = end_month_year.split(" ", maxsplit=1)
                month_name, year = month_year.rsplit(maxsplit=1)
                months = {
                    "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
                    "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноя": 11, "дек": 12
                }
                month = months.get(month_name.lower())
                start_date_str = f"{start_day} — {month} {year}"
                end_date_str = f"{end_day} {month} {year}"
                start_date = datetime.strptime(start_date_str, "%d — %m %Y")
                end_date = datetime.strptime(end_date_str, "%d %m %Y")
            else:
                print("Date format not as expected.")
                start_date, end_date = None, None
        else:
            start_date, end_date = None, None
    
        duration_element = soup.select_one("p.heading:-soup-contains('Длительность') + p.title i.icon-duration")
        duration_text = duration_element.find_next_sibling(string=True).strip() if duration_element else None
        duration = int(duration_text) if duration_text and duration_text.isdigit() else None
    
        details_block = soup.find("div", class_="block mt-6")
        details = details_block.find("div").text.strip() if details_block else None
    
        print(f"Title of {url}: {title}")
    
        # Парсинг по словам
        word_count = {}
        if details:
            words = re.findall(r'\w+', details.lower())
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            print("Word count:", word_count)
    
        db = SessionLocal()
        db.add(Trip(title=title, departure_location=departure_location,
                    start_date=start_date, end_date=end_date,
                    duration=duration, details=json.dumps(word_count)))  # Сохраняем в формате JSON
        db.commit()
        db.close()
    
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for {url}: {execution_time} seconds")
    
    
    async def main():
        urls = [
            "https://turclub-pik.ru/pohod/yaponiya-v-sezon-cveteniya-sakury/",
            "https://www.trip.com/travel-guide/attraction/tokyo/warner-bros-studio-tour-tokyo-the-making-of-harry-potter-136452473/?locale=en-XX&curr=USD",
            "https://turclub-pik.ru/pohod/elbrus-s-yuga-s-komfortom-s-otelem/#trip-4253",
    
        ]
        tasks = []
        for url in urls:
            task = parse_and_save(url)
            tasks.append(task)
        await asyncio.gather(*tasks)
    
    
    if __name__ == "__main__":
        start_time = time.time()
        asyncio.run(main())
        end_time = time.time()
        total_execution_time = end_time - start_time
        print(f"Общее время: {total_execution_time} секунд")

process.py:

    import multiprocessing
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import sessionmaker
from database import Trip, SessionLocal
import time
from datetime import datetime
import re
import json


def parse_and_save(url):
    start_time = time.time()

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string

    departure_location_element = soup.find("div", class_="tags")
    departure_location = departure_location_element.find("a",
                                                         class_="tag has-icon-location").text.strip() if departure_location_element else "Unknown"

    date_option = soup.select_one("option[selected='selected']")
    if date_option:
        date_text = date_option.text.strip()
        if " — " in date_text and " " in date_text:
            start_day, end_month_year = date_text.split(" — ", maxsplit=1)
            end_day, month_year = end_month_year.split(" ", maxsplit=1)
            month_name, year = month_year.rsplit(maxsplit=1)
            months = {
                "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
                "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
            }
            month = months.get(month_name.lower())
            start_date_str = f"{start_day} — {month} {year}"
            end_date_str = f"{end_day} {month} {year}"
            start_date = datetime.strptime(start_date_str, "%d — %m %Y")
            end_date = datetime.strptime(end_date_str, "%d %m %Y")
        else:
            print("Date format not as expected.")
            start_date, end_date = None, None
    else:
        start_date, end_date = None, None

    duration_element = soup.select_one("p.heading:-soup-contains('Длительность') + p.title i.icon-duration")
    duration_text = duration_element.find_next_sibling(text=True).strip() if duration_element else None
    duration = int(duration_text) if duration_text and duration_text.isdigit() else None

    details_block = soup.find("div", class_="block mt-6")
    details = details_block.find("div").text.strip() if details_block else None

    print(f"Title of {url}: {title}")

    # Parsing by words
    word_count = {}
    if details:
        words = re.findall(r'\w+', details.lower())
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        print("Word count:", word_count)

    db = SessionLocal()
    db.add(Trip(title=title, departure_location=departure_location,
                start_date=start_date, end_date=end_date,
                duration=duration, details=json.dumps(word_count)))  # Saving in JSON format
    db.commit()
    db.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for {url}: {execution_time} seconds")


if __name__ == "__main__":
    urls = [
        "https://turclub-pik.ru/pohod/yaponiya-v-sezon-cveteniya-sakury/",
        "https://www.trip.com/travel-guide/attraction/tokyo/warner-bros-studio-tour-tokyo-the-making-of-harry-potter-136452473/?locale=en-XX&curr=USD",
        "https://turclub-pik.ru/pohod/elbrus-s-yuga-s-komfortom-s-otelem/#trip-4253",
        "https://www.tsarvisit.com/ru/visit/zimnie-katanija-na-sobach-ih-uprjazhkah-s-posescheniem-fermy-i-tradicionnym-obedom-671"
    ]

    start_time = time.time()

    processes = []
    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    total_execution_time = end_time - start_time
    print(f"Total execution time: {total_execution_time} seconds")


thread.py:

    import json
    import re
    import threading
    import requests
    from bs4 import BeautifulSoup
    from sqlalchemy import create_engine, Column, Integer, String, DateTime
    from sqlalchemy.orm import sessionmaker
    from database import Trip, SessionLocal
    import time
    from datetime import datetime
    
    
    def parse_and_save(url):
        start_time = time.time()
    
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
    
        departure_location_element = soup.find("div", class_="tags")
        if departure_location_element:
            departure_location_element = departure_location_element.find("a", class_="tag has-icon-location")
        departure_location = departure_location_element.text.strip() if departure_location_element else "Unknown"
    
        date_option = soup.select_one("option[selected='selected']")
        if date_option:
            date_text = date_option.text.strip()
            if " — " in date_text and " " in date_text:
                start_day, end_month_year = date_text.split(" — ", maxsplit=1)
                end_day, month_year = end_month_year.split(" ", maxsplit=1)
                month_name, year = month_year.rsplit(maxsplit=1)
                months = {
                    "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
                    "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
                }
                month = months.get(month_name, None)
                if month:
                    start_date_str = f"{start_day} — {month} {year}"
                    end_date_str = f"{end_day} {month} {year}"
                    start_date = datetime.strptime(start_date_str, "%d — %m %Y")
                    end_date = datetime.strptime(end_date_str, "%d %m %Y")
                else:
                    print("Invalid month name:", month_name)
                    start_date, end_date = None, None
            else:
                print("Date format not as expected.")
                start_date, end_date = None, None
        else:
            start_date, end_date = None, None
    
        duration_element = soup.select_one("p.heading:-soup-contains('Длительность') + p.title i.icon-duration")
        duration_text = duration_element.find_next_sibling(text=True).strip() if duration_element else None
        duration = int(duration_text) if duration_text and duration_text.isdigit() else None
    
        details_block = soup.find("div", class_="block mt-6")
        details = details_block.find("div").text.strip() if details_block else None
    
        print(f"Title of {url}: {title}")
    
        # Word count parsing
        word_count = {}
        if details:
            words = re.findall(r'\w+', details.lower())
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            print("Word count:", word_count)
    
        db = SessionLocal()
        db.add(Trip(title=title, departure_location=departure_location,
                    start_date=start_date, end_date=end_date,
                    duration=duration, details=json.dumps(word_count)))
        db.commit()
        db.close()
    
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for {url}: {execution_time} seconds")
    
    
    urls = ["https://turclub-pik.ru/pohod/yaponiya-v-sezon-cveteniya-sakury/",
            "https://www.trip.com/travel-guide/attraction/tokyo/warner-bros-studio-tour-tokyo-the-making-of-harry-potter-136452473/?locale=en-XX&curr=USD",
            "https://turclub-pik.ru/pohod/elbrus-s-yuga-s-komfortom-s-otelem/#trip-4253",
            "https://www.tsarvisit.com/ru/visit/zimnie-katanija-na-sobach-ih-uprjazhkah-s-posescheniem-fermy-i-tradicionnym-obedom-671"
       ]
    
    start_time = time.time()
    
    threads = []
    
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_execution_time = end_time - start_time
    print(f"Total execution time for all threads: {total_execution_time} seconds")


Используемые подходы:

Asyncio:
Используется для асинхронного выполнения запросов к веб-сайтам и параллельной обработки полученных данных.
Подход эффективен при работе с I/O-операциями, такими как запросы к веб-серверам, когда задержки возникают из-за ожидания ответа.
В процессе выполнения одновременно выполняются несколько задач, что позволяет сэкономить время.
Для парсинга HTML-страниц используется библиотека aiohttp.

Multiprocessing:
Используется для распараллеливания выполнения парсинга веб-страниц с использованием нескольких процессов.
Подход эффективен при выполнении CPU-интенсивных задач, таких как обработка большого объема данных.
Каждый процесс выполняет парсинг одного URL-адреса независимо друг от друга, что повышает скорость выполнения.
Для парсинга HTML-страниц также используется библиотека requests.

Threading:
Используется для выполнения параллельных потоков парсинга веб-страниц.
Подход позволяет управлять несколькими потоками выполнения в пределах одного процесса.
Каждый поток выполняет парсинг одного URL-адреса, обеспечивая параллельное выполнение задач.
Для парсинга HTML-страниц также используется библиотека requests.

Особенности подходов:

Asyncio:
Основное преимущество - асинхронное выполнение I/O-операций, что позволяет избежать блокировки потоков во время ожидания ответа от веб-сервера.
Однако асинхронный подход требует использования асинхронных библиотек и интеграции синхронного кода с асинхронной моделью выполнения.

Multiprocessing:
Эффективен при выполнении CPU-интенсивных задач, так как использует несколько процессов, каждый из которых выполняется на отдельном ядре процессора.
В некоторых случаях может быть сложно управлять общими ресурсами и данными между процессами из-за необходимости использования механизмов синхронизации.

Threading:
Подходит для асинхронной обработки нескольких задач в пределах одного процесса.
Однако из-за GIL (Global Interpreter Lock) в Python потоки не могут полностью параллельно выполняться на многопроцессорных системах.

Время выполнения программ.

Asyncio:
Общее время выполнения: примерно 2.51 секунды.
Преимущественно эффективен для I/O-операций, поскольку выполняет асинхронные запросы к веб-серверам.
Выполняет все задачи параллельно, максимально используя возможности многозадачности.

Multiprocessing:
Общее время выполнения: примерно 4.75 секунд.
Эффективен для CPU-интенсивных задач, таких как парсинг больших объемов данных.
За счет распараллеливания процессов достигается увеличение скорости выполнения, но управление общими ресурсами может быть сложным.

Threading:
Общее время выполнения: примерно 2.64 секунды.
Подходит для параллельной обработки нескольких задач в пределах одного процесса.
Имеет преимущества и недостатки из-за GIL, но в данном случае эффективен для выполнения задач парсинга веб-страниц.

Выводы
Asyncio и Multiprocessing оказались наиболее эффективными для данной задачи.
Asyncio подходит для асинхронных операций ввода-вывода, тогда как Multiprocessing эффективен при работе с CPU-интенсивными задачами.
Threading показал приемлемую производительность, но из-за GIL может быть менее эффективным на многопроцессорных системах.
Итоговая таблица: 

| Задание | async | process             | thread              |
|---------|-------|---------------------|---------------------|
| 1       | 0.04739975929260254 | 0.05212969779968262 | 0.04924564743041992 |
| 2       | 2.5093860626220703  | 4.75020694732666    | 2.6366302967071533  |
