# Лабораторная работа № 2

В данной лабораторной работе было предложено изучить и оценить различные подходы к асинхронному программированию в Python.

## Задача 1

В первой задаче было необходимо разбить вычисление суммы чисел вплоть до 1000000 на подзадачи, используя три разных подхода, и сравнить время выполнения для каждого подхода.

### asyncio
```
async def calc(offset, task_count):
    sum = 0
    for i in range(1 + offset, 1000001, task_count):
        sum += i
    return sum


async def main():
    task_count = 10
    tasks = []

    for i in range(task_count):
        tasks.append(calc(offset=i, task_count=task_count))

    results = await asyncio.gather(*tasks)
    print(sum(results))


if __name__ == "__main__":
    asyncio.run(main())
```

Ключевое слово async показывает, что функция может работать в асинхронном контексте. 
Вычисление разбивается на 10 подзадач, затем результаты собираются в единый массив функцией asyncio.gather(). Ключевое слово await показывает, что во время выполнения каждой подзадачи можно не дожидаться его окончания для перехода к следующей подзадаче.

### threading

```
def calc(offset, task_count, res, index):
    sum = 0
    for i in range(1 + offset, 1000001, task_count):
        sum += i
    res[index] = sum


def main():
    thread_count = 10
    threads = []
    results = [0] * thread_count

    for i in range(thread_count):
        t = threading.Thread(target=calc, args=(i, thread_count, results, i))
        threads.append(t)
        t.start()

    for thr in threads:
        thr.join()
    
    print(sum(results))


if __name__ == "__main__":
    main()
```

В связи с существованием Global Interpreter Lock в Python, истинная многопоточность нам недоступна, в связи с чем данный подход не сильно отличается от asyncio. По сути, реализуется то же самое конкурентное выполнение, так как выполнением всех задач может быть занят только один поток. 
Принцип выполнения аналогичный - задача разбивается на подзадачи, и каждая из них поручается отдельному потоку, каждый из которых добавляет результат выполнения в общий массив, после чего считается итоговая сумма.

### multiprocessing

```
def calc(offset, task_count, queue):
    sum = 0
    for i in range(1 + offset, 1000001, task_count):
        sum += i
    queue.put(sum)


def main():
    process_count = 10
    processes = []
    results = Queue()

    for i in range(process_count):
        p = Process(target=calc, args=(i, process_count, results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    total = 0
    while not results.empty():
        total += results.get()
    
    print(total)


if __name__ == "__main__":
    main()
```
Данный подход кардинально отличается от двух предыдущих по своей сути, и более эффективен он при работе с задачами, нагружающими CPU. Он разбивает задачу на несколько системных процессов, что позволяет использовать многоядерность процессора для параллельного выполнения подзадач. Сам алгоритм при этом схож с предыдущими подходами.

## Итоги выполнения

* multiprocessing - 0.32s
* threading - 0.05s
* asyncio - 0.04s

Ожидаемо, threading и asyncio показали лучшие, примерно одинаковые результаты. Перейдем ко второй задаче, где задействован чуть более сложный процесс, чем выполнение суммы.

## Задача 2

Во второй задаче было необходимо спарсить актуальные для предметной области первой лабораторной данные с нескольких сайтов, разделив парсинг при помощи вышеупомянутых подходов.
Было найдено 2 подходящих для парсинга сайта, с которых собирались названия и описания хакатонов. Так как известный скрапер bs4 отказался работать с multprocessing'ом, а вебдрайвер selenium не поддержал asyncio, было принято решение обращаться непосредственно к ресурсам, откуда берут данные сайты (они динамические и созданы при помощи Тильды). 

### asyncio
```
async def parse_url(url, session):
    async with session.get(url) as resp:
        with psycopg2.connect(host='localhost', database='hackathon_db', user='postgres', password=123, port=5432) as conn:
            with conn.cursor() as cur:
                conn.autocommit = True

                response = await resp.json()

                for post in response['posts']:
                    title = post['title']
                    descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

                    try:
                        data = title, descr
                        cur.execute("INSERT INTO competition (name, description) VALUES ('%s', '%s')" % data)
                            
                    except Exception as e:
                        conn.rollback()
                        print(e)


async def main():
    urls = ["https://feeds.tildacdn.com/api/getfeed/?feeduid=131632209651-986950497851",
        "https://feeds.tildacdn.com/api/getfeed/?feeduid=617755803461"]

    async with aiohttp.ClientSession() as session:
        tasks = [parse_url(url, session) for url in urls]
        await asyncio.gather(*tasks)


if __name__=="__main__":
    asyncio.run(main())
```

Разбиение на подзадачи происходит аналогично задаче 1. При этом для асинхронных запросов к сайтам используется сеанс aiohttp.
Первоначально производится подключение к базе данных и инициализация курсора. Производится запрос к сайту, возвращается ответ в формате json, откуда с легкостью вычленяется название и описание. Затем при помощи курсора выполняется SQL-запрос, вставляющий в базу данных собранные значения.

### threading
```
def parse_url(url, session):
    with psycopg2.connect(host='localhost', database='hackathon_db', user='postgres', password=123, port=5432) as conn:
         with conn.cursor() as cur:
            conn.autocommit = True

            response = session.get(url=url, headers={'User-Agent': 'Mozilla/129.0.2'}).json()

            for post in response['posts']:
                title = post['title']
                descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

                try:
                    data = title, descr
                    cur.execute("INSERT INTO competition (name, description) VALUES ('%s', '%s')" % data)
                    
                except Exception as e:
                    conn.rollback()
                    print(e)


def main():
    urls = ["https://feeds.tildacdn.com/api/getfeed/?feeduid=131632209651-986950497851",
        "https://feeds.tildacdn.com/api/getfeed/?feeduid=617755803461"]

    thread_count = len(urls)
    threads = []
    with requests.Session() as session:
        for i in range(thread_count):
            t = threading.Thread(target=parse_url, args=(urls[i], session))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


if __name__=="__main__":
    main()
```
Threading также функционирует аналогично предыдущей задаче, однако здесь уже используется стандартный объект Session из библиотеки requests. Функция парсинга остается неизменной.

### multiprocessing
```
def parse_url(url, session):
    with psycopg2.connect(host='localhost', database='hackathon_db', user='postgres', password=123, port=5432) as conn:
        with conn.cursor() as cur:
            conn.autocommit = True

            response = session.get(url=url, headers={'User-Agent': 'Mozilla/129.0.2'}).json()

            for post in response['posts']:
                title = post['title']
                descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

                try:
                    data = title, descr
                    cur.execute("INSERT INTO competition (name, description) VALUES ('%s', '%s')" % data)
                    
                except Exception as e:
                    conn.rollback()
                    print(e)


def main():
    urls = ["https://feeds.tildacdn.com/api/getfeed/?feeduid=131632209651-986950497851",
        "https://feeds.tildacdn.com/api/getfeed/?feeduid=617755803461"]

    process_count = len(urls)
    processes = []

    with requests.Session() as session:
        for i in range(process_count):
            p = Process(target=parse_url, args=(urls[i], session))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()


if __name__=="__main__":
    main()
```
Та же история и с мультипроцессингом.

## Итоги выполнения 

Была осуществлена проверка корректности вставки данных через pgAdmin. Временные результаты оказались следующими:

* multiprocessing - 1.4s
* threading - 0.24s
* asyncio - 0.34s

В данном случае threading оказался чуть быстрее, чем asyncio. Multiprocessing же остался сильно позади, поскольку плохо подходит для I/O-bound задач, то есть тех, в которых идет большое количество операций ввода-вывода.

## Выводы
Таким образом, в ходе данной работы были протестированы 3 подхода к конкурентному и параллельному исполнению кода. На основании временных измерений и особенностей каждого подхода для Web-разработки оказался наиболее подходящим метод, задействующий библиотеку asyncio, к тому же, его поддерживает и фреймворк FastAPI.