# ЛР №2

В данной лабораторной работе был разработан парсер, а также была произведена работа с функциями python по выполнению задач в асинхроном режиме.

## Асинхронное программирование

В первой части необходимо использовать функции python, чтобы реализовать выполнение задач в несколько потоков.

### Threading

Разберём один из способов асинхроной работы. 

```python
import threading
from time import time

first_number = 1
last_number = 1000000

NUMBER_OF_THREADS = 4
NUMBERS_FOR_THREAD = last_number // NUMBER_OF_THREADS

results = [0] * NUMBER_OF_THREADS 

# Возвращает сумму чисел от start до end включительно
def calculate_sum(start: int, end: int):
    return sum(range(start, end+1))

# Вызывает функцию calculate_sum и записывает в свою ячейку results
def worker(i: int):
    results[i] = calculate_sum(NUMBERS_FOR_THREAD * i + 1, NUMBERS_FOR_THREAD * (i + 1))
    
# Основной поток
def thread_calculate_sum():
    threads = []
    for i in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Result(thread): " + str(sum(results)))


def non_thread_calculate_sum():
    calculate_sum(first_number, last_number)
    print("Result(non thread): " + str(sum(results)))


if __name__ == "__main__":
    n_tests = 10

    times = []
    for i in range(n_tests):
        start = time()
        thread_calculate_sum()
        end = time()
        times.append(end-start)
    result_avg_time = sum(times)/n_tests
    print("AVG time: " + str(result_avg_time))

    times = []
    for i in range(n_tests):
        start = time()
        non_thread_calculate_sum()
        end = time()
        times.append(end-start)
    result_avg_time = sum(times)/n_tests
    print("AVG time: " + str(result_avg_time))
```

Как можно видеть, мы разбили задачу по вычислению суммы на несколько частей, а также сравнили время выполнения той же задачи, но в синхроном режиме.

По итогам первой части, в которой мы высчитывали время выполнения рассчётов, можно сказать, что асинхронный подход является быстрей, потому что одну задачу мы делим на несколько задач, которые выполняются одновременно.

Если сравнивать способы реализации асинхроного программирования, то можно сказать, что для данной задачи multiprocessing подходит лучше, так как он действительно позволяет разделить задачу на несколько процессов, но конкретно в этой задаче расчёты слишком малы, чтобы он показал своё преимущество.


## Асинхронное программирование с парсером

Теперь реализуем те же самые способы асинхронного программирования для парсера информации с сайта.

Парсер:
```python
# Ebay
def pars_item_ebay(item):
    title_tag = item.find('div', class_="s-item__title")
    title_span = title_tag.find('span', role='heading')
    title_text = title_span.get_text()
    price_tag = item.find('span', class_='s-item__price')
    price_text = price_tag.get_text()
    
    return {'title': title_text, 'price': price_text}

def insert_into_db(parsed_items):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    for item in parsed_items:
        try:
            cursor.execute('''INSERT INTO items (name, price) VALUES (%s, %s)''', (item["title"], item["price"]))
        except:
            continue
    conn.commit()
    cursor.close()
    conn.close()

def parse_and_save(url):
    items = []
    while items == []:
        print("Отправляем запрос")
        try:
            response = requests.get(url)
            print("Status code: " + str(response.status_code))
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            print(f"Error req: {url}\n{e}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Avito
        #items = soup.find_all('div', class_='iva-item-body-GQomw')
        
        # Ebay
        items = soup.find_all('li', class_='s-item')
        
        if items == []:
            print("Не нашлись items")
            f = open("test_results.txt", 'w', encoding="utf-8")
            f.write(str(soup))
            f.close()
            return 0
        
    
    parsed_items = []
    for item in items:
        
        # Avito
        #item_res = pars_item_avito(item)
        
        # Ebay
        item_res = pars_item_ebay(item)
        parsed_items.append(item_res)
    
    #print(parsed_items)
    insert_into_db(parsed_items)
```
### asyncio
Приведём пример работы с модулем asyncio

```python
import asyncio
import aiohttp
from time import time
from bs4 import BeautifulSoup
from parsing import URLS2, pars_item_ebay, insert_into_db

async def fetch(session, url):
    async with session.get(url) as response:
        print("Status code: " + str(response.status))
        return await response.text()

async def parse_and_save(session, url):
    print("Отправляем запрос")
    try:
        text = await fetch(session, url)
    except aiohttp.ClientError as e:
        print(f"Error req: {url}\n{e}")

    soup = BeautifulSoup(text, 'html.parser')
    items = soup.find_all('li', class_='s-item')

    parsed_items = []
    for item in items:
        item_res = pars_item_ebay(item)
        parsed_items.append(item_res)

    insert_into_db(parsed_items)

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = parse_and_save(session, url)
            tasks.append(task)
        await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    start = time()
    asyncio.run(main(URLS2))
    end = time()
    print("Time: " + str(end - start))
```

В данной части работы можно заметить, что выполнение задач при помощи разных модулем происходит примерно за одно и тоже время, но лучше всего происходит у asyncio.

