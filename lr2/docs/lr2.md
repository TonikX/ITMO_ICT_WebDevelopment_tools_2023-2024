# Лабораторная 2
Цель работы: понять отличия потоками и процессами и понять, что такое ассинхронность в Python.

Работа о потоках, процессах и асинхронности поможет студентам развить навыки создания эффективных и быстродействующих программ, что важно для работы с большими объемами данных и выполнения вычислений. Этот опыт также подготавливает студентов к реальным проектам, где требуется использование многопоточности и асинхронности для эффективной обработки данных или взаимодействия с внешними сервисами. Вопросы про потоки, процессы и ассинхронность встречаются, как минимум, на половине собеседований на python-разработчика уровня middle и Выше.

# Задание 1
Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async. Каждая программа должна решать считать сумму всех чисел от 1 до 1000000. Разделите вычисления на несколько параллельных задач для ускорения выполнения.

## Решение


### Threading
Создадим поток для каждого отрезка чисел по 100000. Данный поток выполнит функцию, которая просуммирует все точки данного отрезка и результат добавит в список.
После выполнения всех потоков просуммируем результаты из списка и отобразим их на экране.

```python
import threading

def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.append(total)

def main():
    result = []
    threads = []
    chunk_size = 100000

    for i in range(0, 1000000, chunk_size):
        thread = threading.Thread(
            target=calculate_sum,
            args=(i+1, i+chunk_size+1, result)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Sum:", sum(result))

if __name__ == "__main__":
    main()
```

### Multiprocessing

Решение на основе библиотеки multiprocessing отличается от предыдущего решения лишь необходимостью создания механизма синхронизации значений между потоками, так как они не имеют общих ресурсов.
Для этого создадим объект multiprocessing.Queue, в который будет записывать суммы отрезков.
После успешного выполнения всех процессов, просуммируем все значения и отобразим на экране
```python
import multiprocessing

def calculate_sum(start, end, result):
    total = sum(range(start, end))
    result.put(total)

def main():
    result = multiprocessing.Queue()
    processes = []
    chunk_size = 100000

    for i in range(0, 1000000, chunk_size):
        process = multiprocessing.Process(
            target=calculate_sum,
            args=(i+1, i+chunk_size+1, result)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_sum = 0
    while not result.empty():
        final_sum += result.get()

    print("Sum:", final_sum)

if __name__ == "__main__":
    main()
```

### Asyncio

Напишем асинхронный код для нахождение суммы. Для этого объявим нашу функцию calculate_sum как корутину. Затем для каждого отрезка создадим asyncio Task и дождемся их выполнения. После этого отобразим сумму результатов на экране.

```python
import asyncio

async def calculate_sum(start, end):
    return sum(range(start, end))

async def main():
    chunk_size = 100000
    tasks = []

    for i in range(0, 1000000, chunk_size):
        task = asyncio.create_task(calculate_sum(i+1, i+chunk_size+1))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    print("Sum:", sum(results))

if __name__ == "__main__":
    asyncio.run(main())
```

### Benchmark
Напишем небольшой benchmark для сравнения времени работы различных подходов, описанных ранее.

```python
import time
import asyncio as aio
from sum_threading import main as threading_main
from sum_mp import main as multiprocessing_main
from sum_aio import main as asyncio_main
from functools import partial

def benchmark(function, name):
    start_time = time.perf_counter()
    function()
    end_time = time.perf_counter()
    print(f"{name} took {end_time - start_time:.4f} seconds")

def main():
    print("Benchmarking threading...")
    benchmark(threading_main, "Threading")

    print("\nBenchmarking multiprocessing...")
    benchmark(multiprocessing_main, "Multiprocessing")

    print("\nBenchmarking asyncio...")
    benchmark(partial(aio.run, asyncio_main()), "Asyncio")

if __name__ == "__main__":
    main()
```

Запустим данную программу и получим следующий результат:
```
Benchmarking threading...
Sum: 500000500000
Threading took 0.0136 seconds

Benchmarking multiprocessing...
Sum: 500000500000
Multiprocessing took 0.1534 seconds

Benchmarking asyncio...
Sum: 500000500000
Asyncio took 0.0123 seconds
```

Заметим, что вариант с библиотекой multiprocessing работал дольше всего из-за необходимости создания отдельного процесса.

Вариант с потоками немного медленнее асинхронного кода из-за необходимости создания потоков.

Асинхронный вариант работает быстрее всего из-за того, что все выполняется в одном потоке.


# Задание 2
Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

## Решение

### Парсеры
1. Создадим абстрактный класс парсера, который определит синхронный и асинхронный метод для парсинга транзакций

```python
class AbstractParser(ABC):
    base_url: str

    @abstractmethod
    def parse(self) -> list[Transaction]:
        ...
    
    @abstractmethod
    async def aio_parse(self) -> list[Transaction]:
        ...
```

2. Создадим базовый класс парсера, который будет определять методы для скачивания данных с ресурса и вызова методов для парсинга
```python
class BaseParser(AbstractParser):
    base_url: str

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(requests.get(self.base_url).text, "html.parser")

    async def aio_get_soup(self) -> BeautifulSoup:
        async with aiohttp.ClientSession() as client:
            async with client.get(self.base_url) as resp:
                return BeautifulSoup(await resp.read(), "html.parser")

    def parse(self) -> list[Transaction]:
        return self._parse(self.get_soup())
    
    async def aio_parse(self) -> list[Transaction]:
        return self._parse(await self.aio_get_soup())
```

3. Создадим класс для сбора транзакция с сайта [blockhain.com](https://www.blockchain.com/explorer/mempool/btc)

```python
class BlockchainComParser(BaseParser):
    def __init__(self):
        self.base_url = "https://www.blockchain.com/explorer/mempool/btc"
    
    def _parse(self, soup: BeautifulSoup):
        el = soup.find("div", class_="sc-7b53084c-1")
        trs = []
        for transaction in el:
            tr_hash = os.path.basename(transaction["href"])
            timestamp = datetime.strptime(transaction.find("div", class_="sc-35e7dcf5-7").text, "%m/%d/%Y, %H:%M:%S")
            amount = float(transaction.find("div", class_="sc-35e7dcf5-13").text.split()[0])
            trs.append(Transaction(transaction_id=int(tr_hash, 16), user_id=1, amount=amount, transaction_type="transfer", category_id=1, timestamp=timestamp))
        return trs
```

4. Создадим класс для сбора транзакций с сайта [btc.com](https://explorer.btc.com/btc/unconfirmed-txs)

```python
class BtcComParser(BaseParser):
    def __init__(self) -> None:
        self.base_url = "https://explorer.btc.com/btc/unconfirmed-txs"

    def _parse(self, soup: BeautifulSoup) -> list[Transaction]:
        table = soup.find("table")
        tbody = table.find("tbody")
        trs = []
        for row in tbody:
            tx_hash, timestamp, _, output_volume, _, _ = row.find_all("td")
            tx_hash = os.path.basename(tx_hash.find("a")["href"])
            trs.append(Transaction(
                transaction_id=int(tx_hash, 16),
                user_id=1,
                amount=float(output_volume.text.split()[0]),
                transaction_type="transfer",
                category_id=1,
                timestamp=datetime.strptime(timestamp.text, "%Y-%m-%d %H:%M:%S")
            ))
        return trs
```

### parse_and_save

1. Напишем код для парсинга данных из разных потоков. В каждый поток мы будем передавать объект класса парсера и в данном потоке будем сохранять результаты в базу данных

```python
import threading
from conn import get_session
from sqlmodel import Session
from parsers import BlockchainComParser, BtcComParser, AbstractParser

def parse_and_save(parser: AbstractParser, session: Session):
    parsed_data = parser.parse()
    for d in parsed_data:
        session.add(d)

def main():
    blockchain_parser = BlockchainComParser()
    btc_parser = BtcComParser()
    session = next(get_session())
    thread1 = threading.Thread(target=parse_and_save, args=(blockchain_parser, session))
    thread2 = threading.Thread(target=parse_and_save, args=(btc_parser, session))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
```

2. Напишем код для парсинга данных из разных процессов. В данном случае нам необходимо создавать сессию подключения к базе данных внутри функции parse_and_save из-за того, что объект Session нельзя кодировать при помощи pickle.

```python
import multiprocessing
from conn import get_session
from parsers import BlockchainComParser, BtcComParser, AbstractParser

def parse_and_save(parser: AbstractParser):
    parsed_data = parser.parse()
    session = next(get_session())
    for d in parsed_data:
        session.add(d)

def main():
    blockchain_parser = BlockchainComParser()
    btc_parser = BtcComParser()
    process1 = multiprocessing.Process(target=parse_and_save, args=(blockchain_parser,))
    process2 = multiprocessing.Process(target=parse_and_save, args=(btc_parser,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()

if __name__ == "__main__":
    main()
```

3. Напишем код для парсинга данных при помощи асинхронных функций. В данном случае нам необходимо написать дополнительный код, который будет создавать асинхронное подключение к базе данных

```python
import os
from dotenv import load_dotenv

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker


load_dotenv()
engine = create_async_engine(os.getenv("ASYNC_DB_URL"), echo=True, future=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
```

Затем напишем код, который создаст несколько объектов asyncio.Task и дождется их выполнения.

```python
import asyncio as aio
from aio_conn import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from parsers import BlockchainComParser, BtcComParser, AbstractParser

async def parse_and_save(parser: AbstractParser, session: AsyncSession):
    parsed_data = await parser.aio_parse()
    for d in parsed_data:
        session.add(d)

async def main():
    blockchain_parser = BlockchainComParser()
    btc_parser = BtcComParser()
    session = await anext(get_session())
    task1 = aio.create_task(parse_and_save(blockchain_parser, session))
    task2 = aio.create_task(parse_and_save(btc_parser, session))
    await aio.gather(task1, task2)

if __name__ == "__main__":
    aio.run(main())
```

### Benchmark

Немного изменим код из Задания 1 для того, чтобы провести benchmark полученных решений.

```python
import time
import asyncio as aio
from parse_threading import main as threading_main
from parse_mp import main as multiprocessing_main
from parse_aio import main as asyncio_main
from functools import partial

def benchmark(function, name):
    start_time = time.perf_counter()
    function()
    end_time = time.perf_counter()
    print(f"{name} took {end_time - start_time:.4f} seconds")

def main():
    print("Benchmarking threading...")
    benchmark(threading_main, "Threading")

    print("\nBenchmarking multiprocessing...")
    benchmark(multiprocessing_main, "Multiprocessing")

    print("\nBenchmarking asyncio...")
    benchmark(partial(aio.run, asyncio_main()), "Asyncio")

if __name__ == "__main__":
    main()
```

```
Benchmarking threading...
Threading took 0.4149 seconds

Benchmarking multiprocessing...
Multiprocessing took 0.8405 seconds

Benchmarking asyncio...
Asyncio took 0.4639 seconds
```

В данном задании у нас решение с библотекой multiprocessing получилось самым медленным. Так произошло из-за того, что количество сайтов не такое большое и overhead от создания новых процессов сильно влияет на производительность.

Асинхронное решение сработало хуже, чем threading. Так произошло, скорее всего, из-за синхронной функции _parse, которая блокирует выполнение.