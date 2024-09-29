# Задание 1 
При реализации всех подходов в данном задании использовалась следующая стратегия: 
пользователю предлагается ввести число. Далее числовой промежуток разбивается на 
данное число промежутков и отдельный поток вычисляет каждый промежуток. 
Затем результат суммируется 

## threading 
```python
import threading

total_sum = 0


def calculate_sum(left: int, right: int):
    global total_sum
    local_sum = 0
    for i in range(left, right+1):
        local_sum += i
        
    total_sum += local_sum


def main():
    n = int(input("Укажите степень параллелизма "))
    threads = []

    top_border = 1000000
    step = top_border // n

    for i in range(1, n+1):
        right_border = step*i
        left_border = right_border-step+1
        t = threading.Thread(target=calculate_sum, args=(left_border, right_border,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Total sum equal: ", total_sum)

main()
```

## processing 
```python
import multiprocessing as mp


def calculate_sum(q, left: int, right: int):
    local_sum = 0
    for i in range(left, right + 1):
        local_sum += i

    total_sum = q.get()
    total_sum += local_sum
    q.put(total_sum)


def main():
    n = int(input("Укажите степень параллелизма "))
    processes = []

    top_border = 1000000
    step = top_border // n

    q = mp.Queue()
    q.put(0)

    for i in range(1, n+1):
        right_border = step*i
        left_border = right_border-step+1
        p = mp.Process(target=calculate_sum, args=(q, left_border, right_border,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_sum = q.get()
    print("Total sum equal: ", total_sum)


if __name__ == '__main__':
    main()
    
```

## async 
```python
import asyncio

total_sum = 0


async def calculate_sum(left: int, right: int):
    global total_sum
    local_sum = 0
    for i in range(left, right + 1):
        local_sum += i

    total_sum += local_sum


async def main():
    n = int(input("Укажите степень параллелизма "))

    top_border = 1000000
    step = top_border // n

    for i in range(1, n + 1):
        right_border = step * i
        left_border = right_border - step + 1
        t = asyncio.create_task(calculate_sum(left_border, right_border))
        await t

    print("Total sum equal: ", total_sum)

asyncio.run(main())
```

# Задание 2 
В данном задании использовался паттерн "пул потоков".
Пользователь так же вводит степень парраллелизма. Создается соот. число потоков
и каждый из них делает свою часть работы

## threading 
```python
import threading as t
import requests
from bs4 import BeautifulSoup

database = {}

work = [
    "https://www.gismeteo.ru/diary/4079/2023/2/",
    "https://www.w3schools.com/html/html_basic.asp",
    "https://www.javatpoint.com/simple-html-pages"
]
lock = t.Lock()


def parse_and_save(url):
    global database
    headers = {
        'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
    }

    response = requests.get(url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page)
    title = soup.title.text
    database[url] = title


def acquire_work():
    global work

    while True:
        lock.acquire()
        if work:
            url = work[0]
            work.pop(0)
            lock.release()
            parse_and_save(url)
        else:
            lock.release()
            return


def main(n: int):
    workers = []
    for _ in range(n):
        worker = t.Thread(target=acquire_work)
        workers.append(worker)
        worker.start()

    for w in workers:
        w.join()

    print(database)


main(3)
```

## processing 
```python
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup


def parse_and_save(url):
    headers = {
        'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
    }

    response = requests.get(url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page)
    title = soup.title.text
    return url, title


if __name__ == "__main__":
    n = 3
    with Pool(processes=n) as pool:
        work = [
            "https://www.gismeteo.ru/diary/4079/2023/2/",
            "https://www.w3schools.com/html/html_basic.asp",
            "https://www.javatpoint.com/simple-html-pages"
        ]
        result = pool.map(parse_and_save, work)
        print(result)

```

## async 
```python
import asyncio
import threading as t
import requests
from bs4 import BeautifulSoup

database = {}

work = [
    "https://www.gismeteo.ru/diary/4079/2023/2/",
    "https://www.w3schools.com/html/html_basic.asp",
    "https://www.javatpoint.com/simple-html-pages"
]
lock = asyncio.Lock()


def parse_and_save(url):
    global database
    headers = {
        'User-Agent': 'My User Agent 1.0',  # многие сайты не дают себя парсить ботам
    }

    response = requests.get(url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page)
    title = soup.title.text
    database[url] = title


async def acquire_work():
    global work

    while True:
        await lock.acquire()
        if work:
            url = work[0]
            work.pop(0)
            lock.release()
            parse_and_save(url)
        else:
            lock.release()
            return


async def main(n: int):
    for _ in range(n):
        worker = asyncio.create_task(acquire_work())
        await worker

    print(database)


asyncio.run(main(3))
```
