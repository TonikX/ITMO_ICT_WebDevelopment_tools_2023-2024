# Отчет по лабораторной работе №2

#### Цель работы:

Научиться работать с асинхронным кодом, управлять потоками и процессами в языке python.

## Задание

#### Текст задания:

1. Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.
2. Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

#### Ход Работы:

Для первого задания я написал три скрипта, для суммирования чисел от 1 до 1000000:

1. Выделение потоков для суммирования:

```
    for i in range(NUM_THREADS):
    start = i * (TOTAL // NUM_THREADS) + 1
    end = (i + 1) * (TOTAL // NUM_THREADS)
    thread = threading.Thread(target=calculate_sum, args=(start, end, result))
    threads.append(thread)
    thread.start()
```

2. Выделение процессов для суммирования:

```
    for url in urls:
    process = multiprocessing.Process(target=parse_and_save, args=(url,))
    processes.append(process)
    process.start()
```

3. Асинхронный подход:

```
    tasks = []

    for i in range(NUM_TASKS):
        start = i * (TOTAL // NUM_TASKS) + 1
        end = (i + 1) * (TOTAL // NUM_TASKS)
        tasks.append(calculate_sum(start, end))

    partial_sums = await asyncio.gather(*tasks)
```

После выполнения каждого из них получились следующие результаты:

|Потоки|Процессы|Асинхронный код|
|-|--------|---|
|0.02946949005126953|0.20459461212158203|0.02500128746032715|

Вывод:
В данном случае, несмотря на результат, правильнее было бы использовать потоки, так как все асинхронные задачи
все равно будут выполняться последовательно, потому что мы блокируем поток операциями суммы. Однако в виду небольшого числа 1000000, выделение потоков и процессов заняло куда больше времени чем обычное выполнение кода, однако при сильном увеличении числа N - код на потоках будет более быстрым.

Для второго задания я создал файл database.py, где инкапсулирована логика взаимодействия с базой данных

```
def create_session() -> Session:
    return Session(bind=engine)

class Article(SQLModel, table=True):
    id: int = Field(primary_key=True)
    article: str = Field()

def commit_article(title: str):
    db_session = create_session()
    db_article = Article(article=title)

    db_session.add(db_article)
    db_session.commit() 
    db_session.refresh(db_article)
```

И позже имплементировал его в каждый парсер сайтов:

асинхронных код:

```
async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, 'html.parser')
        title = parsed_html.title.string
        commit_article(title)


async def main():
    urls = ["https://zoom.us/", "https://www.skype.com/", "https://discord.com/"]

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)
```

потоки:

```
def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string
    commit_article(title)


def main():
    urls = ["https://zoom.us/", "https://www.skype.com/", "https://discord.com/"]

    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
```

процессы:

```
def parse_and_save(url):
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text, 'html.parser')
    title = parsed_html.title.string
    commit_article(title)


def main():
    urls = ["https://zoom.us/", "https://www.skype.com/", "https://discord.com/"]

    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
```

После запуска программ получились следующие результаты:

|Потоки|Процессы|Асинхронный код|
|-|--------|---|
|1.2561585903167725|2.2433619499206543|0.6306295394897461|

Ожидаемо асинхронный подход лучше всех себя показал, так как параллельно отправил запросы на получение html страниц и после распарсих их. Использование потоков и процессов тут нежелательно.

Все записи добавились в базу данных:
![alt text](image.png)

## Вывод

В ходе работы научился создавать потоки и процессы овладел конструкцией async await, смог количественно оценить время выполнения одинковых задач, реализованных каждым из этих методов
