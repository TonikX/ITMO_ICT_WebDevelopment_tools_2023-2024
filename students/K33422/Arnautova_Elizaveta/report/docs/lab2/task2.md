**Задача 2. Параллельный парсинг веб-страниц с сохранением в базу данных**

**Задача:** Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

**Подробности задания:**

- Напишите три различных программы на Python, использующие каждый из подходов: threading, multiprocessing и async.
- Каждая программа должна содержать функцию parse_and_save(url), которая будет загружать HTML-страницу по указанному URL, парсить ее, сохранять заголовок страницы в базу данных и выводить результат на экран.
- Используйте базу данных из лабораторной работы номер 1 для заполенния ее данными. Если Вы не понимаете, какие таблицы и откуда Вы могли бы заполнить с помощью парсинга, напишите преподавателю в общем чате потока.
- Для threading используйте модуль threading, для multiprocessing - модуль multiprocessing, а для async - ключевые слова async/await и модуль aiohttp для асинхронных запросов.
- Создайте список нескольких URL-адресов веб-страниц для парсинга и разделите его на равные части для параллельного парсинга.
- Запустите параллельный парсинг для каждой программы и сохраните данные в базу данных.
- Замерьте время выполнения каждой программы и сравните результаты.


**naive**
```python
from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import re


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conn = psycopg2.connect("dbname=recipes user=postgres password=12345678 host=localhost")
    curs = conn.cursor()

    recipe_blocks = soup.find_all('div', class_='emotion-etyz2y')

    for block in recipe_blocks:
        try:
            title = block.find('span', class_="emotion-1bs2jj2").text
            ingredients_text = block.find('button', class_="emotion-d6nx0p").text
            servings_text = block.find('span', class_="emotion-tqfyce").text[0]
            cook_time = block.find('span', class_="emotion-14gsni6").text
            author = block.find('span', class_="emotion-14tqfr").text.replace("Автор:", "").strip()
            servings = int(re.search(r'\d+', servings_text).group())
            ingredients = int(re.search(r'\d+', ingredients_text).group())

            curs.execute("INSERT INTO titles (url, title, ingredients, servings, cook_time, author) VALUES (%s, %s, %s, %s, %s, %s)",
                     (url, title, ingredients, servings, cook_time, author))
            conn.commit()
            # print(f"Saved: {title} | Ingredients: {ingredients} | Servings: {servings} | Cook time: {cook_time}")
        except AttributeError as e:
            print(f"Failed to parse block: {e}")

    curs.close()
    conn.close()


if __name__ == "__main__":
    urls = [
        'https://eda.ru/recepty/zavtraki',
        'https://eda.ru/recepty/osnovnye-blyuda',
        'https://eda.ru/recepty/sousy-marinady',
        'https://eda.ru/recepty/zagotovki',
        'https://eda.ru/recepty/bulony',
        'https://eda.ru/recepty/pasta-picca',
        'https://eda.ru/recepty/supy',
        'https://eda.ru/recepty/zakuski',
        'https://eda.ru/recepty/rizotto',
        'https://eda.ru/recepty/sendvichi',
        'https://eda.ru/recepty/napitki',
        'https://eda.ru/recepty/salaty',
        'https://eda.ru/recepty/vypechka-deserty',

    ]

    start_time = time.time()
    for url in urls:
        parse_and_save(url)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Threading execution time: {execution_time:.4f} seconds")

```

**threading**
```python
from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import re


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conn = psycopg2.connect("dbname=recipes user=postgres password=12345678 host=localhost")
    curs = conn.cursor()

    recipe_blocks = soup.find_all('div', class_='emotion-etyz2y')

    for block in recipe_blocks:
        try:
            title = block.find('span', class_="emotion-1bs2jj2").text
            ingredients_text = block.find('button', class_="emotion-d6nx0p").text
            servings_text = block.find('span', class_="emotion-tqfyce").text[0]
            cook_time = block.find('span', class_="emotion-14gsni6").text
            author = block.find('span', class_="emotion-14tqfr").text.replace("Автор:", "").strip()
            servings = int(re.search(r'\d+', servings_text).group())
            ingredients = int(re.search(r'\d+', ingredients_text).group())

            curs.execute("INSERT INTO titles (url, title, ingredients, servings, cook_time, author) VALUES (%s, %s, %s, %s, %s, %s)",
                     (url, title, ingredients, servings, cook_time, author))
            conn.commit()
            # print(f"Saved: {title} | Ingredients: {ingredients} | Servings: {servings} | Cook time: {cook_time}")
        except AttributeError as e:
            print(f"Failed to parse block: {e}")

    curs.close()
    conn.close()


def main(urls):
    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    urls = [
        'https://eda.ru/recepty/zavtraki',
        'https://eda.ru/recepty/osnovnye-blyuda',
        'https://eda.ru/recepty/sousy-marinady',
        'https://eda.ru/recepty/zagotovki',
        'https://eda.ru/recepty/bulony',
        'https://eda.ru/recepty/pasta-picca',
        'https://eda.ru/recepty/supy',
        'https://eda.ru/recepty/zakuski',
        'https://eda.ru/recepty/rizotto',
        'https://eda.ru/recepty/sendvichi',
        'https://eda.ru/recepty/napitki',
        'https://eda.ru/recepty/salaty',
        'https://eda.ru/recepty/vypechka-deserty',

    ]

    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Threading execution time: {execution_time:.4f} seconds")

```

**multiprocessing**
```python
from multiprocessing import Process
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import re


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    conn = psycopg2.connect("dbname=recipes user=postgres password=12345678 host=localhost")
    curs = conn.cursor()

    recipe_blocks = soup.find_all('div', class_='emotion-etyz2y')

    for block in recipe_blocks:
        try:
            title = block.find('span', class_="emotion-1bs2jj2").text
            ingredients_text = block.find('button', class_="emotion-d6nx0p").text
            servings_text = block.find('span', class_="emotion-tqfyce").text[0]
            cook_time = block.find('span', class_="emotion-14gsni6").text
            author = block.find('span', class_="emotion-14tqfr").text.replace("Автор:", "").strip()
            servings = int(re.search(r'\d+', servings_text).group())
            ingredients = int(re.search(r'\d+', ingredients_text).group())

            curs.execute(
                "INSERT INTO titles (url, title, ingredients, servings, cook_time, author) VALUES (%s, %s, %s, %s, %s, %s)",
                (url, title, ingredients, servings, cook_time, author))
            # print(f"Saved: {title} | Ingredients: {ingredients} | Servings: {servings} | Cook time: {cook_time}")

        except AttributeError as e:
            print(f"Failed to parse block: {e}")

    curs.close()
    conn.close()


def main(urls):
    processes = []
    for url in urls:
        process = Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    urls = [
        'https://eda.ru/recepty/zavtraki',
        'https://eda.ru/recepty/osnovnye-blyuda',
        'https://eda.ru/recepty/sousy-marinady',
        'https://eda.ru/recepty/zagotovki',
        'https://eda.ru/recepty/bulony',
        'https://eda.ru/recepty/pasta-picca',
        'https://eda.ru/recepty/supy',
        'https://eda.ru/recepty/zakuski',
        'https://eda.ru/recepty/rizotto',
        'https://eda.ru/recepty/sendvichi',
        'https://eda.ru/recepty/napitki',
        'https://eda.ru/recepty/salaty',
        'https://eda.ru/recepty/vypechka-deserty',
    ]

    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Multiprocessing execution time: {execution_time:.4f} seconds")

```

**asyncio**
```python
import asyncio
import time


async def calculate_sum(start, end):
    total = sum(x * x for x in range(start, end))
    return total


async def main():
    num_tasks = 10
    range_per_task = 10 ** 6 // num_tasks
    times = 10

    av_time = 0
    for i in range(times):
        tasks = [calculate_sum(i * range_per_task, (i + 1) * range_per_task) for i in range(num_tasks)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_sum = sum(results)
        end_time = time.time()

        av_time = av_time + end_time - start_time

    print(f"Asyncio total sum: {total_sum}")
    print(f"Asyncio execution time: {av_time/times:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main())

```

Здесь уже не стала автоматизировать прогон N-раз, просто прогнала вручную, чтобы проверить и вычислить погрешность.

<table>
  <thead>
    <tr>
      <th></th>
      <th>Naive</th>
      <th>Threading</th>
      <th>Multiprocessing</th>
      <th>Asyncio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Time</th>
      <td>7.6552 ± 3.2</td>
      <td>1.4692 ± 0.4</td>
      <td>1.4662 ± 0.3</td>
      <td>1.3968 ± 0.3</td>
    </tr>
  </tbody>
</table>

Тут уже наивный алгоритм перестает справляться. И это особенно колоритно в погрешности: если у async, multiprocessing и threading речь идет про десятые секунды, то для наивного разница исчисляется уже в секундах.

Для моих данных несильно, но, все же, лучше, отработал Asyncio.


**Threading (Многопоточность)**
```
Особенности:
* Многопоточность позволяет выполнять несколько потоков в рамках одного процесса.
* Все потоки делят между собой одно и то же пространство памяти.
* Потоки выполняются параллельно, но из-за GIL (Global Interpreter Lock) в Python 
только один поток может выполнять Python код в любой момент времени.
* Подходит для задач, связанных с вводом-выводом (I/O-bound), например, сетевые запросы, 
чтение/запись файлов, ожидание ответов от баз данных.

Когда лучше использовать:
* Задачи, которые требуют ожидания внешних ресурсов.
* Когда нужно выполнить параллельно много операций ввода-вывода.

Пример: сетевые запросы, работа с файлами.
```

**Multiprocessing (Многопроцессорность)**
```
Особенности:

* Многопроцессорность позволяет создавать несколько процессов, 
каждый из которых имеет свое собственное пространство памяти.
* Не ограничен GIL, так как каждый процесс исполняется независимо.
* Подходит для задач, связанных с интенсивными вычислениями (CPU-bound).

Когда лучше использовать:
* Задачи, требующие значительных вычислительных ресурсов.
* Обработка данных, научные вычисления, машинное обучение.

Пример: параллельная обработка больших объемов данных.
```

**Async (Асинхронное программирование)**
```
Особенности:
* Асинхронное программирование позволяет выполнять операции ввода-вывода 
асинхронно, не блокируя основной поток выполнения.
* Использует event loop (цикл событий) для управления задачами.
* Подходит для задач ввода-вывода с высокой задержкой, где блокировка основного потока 
нежелательна.

Когда лучше использовать:
* Сетевые приложения, работа с веб-серверами.
* Когда требуется одновременное выполнение множества I/O операций с минимальными задержками.

Пример: асинхронные веб-серверы, асинхронные клиентские запросы.
```

**Различия во времени выполнения**

- Threading может быть медленнее из-за GIL, если задачи CPU-bound. Но для I/O-bound задач (например, сетевые запросы) многопоточность может значительно уменьшить время ожидания.
- Multiprocessing не ограничен GIL, поэтому для CPU-bound задач он будет быстрее, чем threading. Однако создание и управление процессами требует больше ресурсов и времени, чем создание потоков.
- Async наиболее эффективен для большого количества I/O-bound задач, так как позволяет избежать блокировки и максимально использовать время ожидания.

**Выводы**

- Использовать threading, если много задач на ввод-вывод => упростить код за счет параллельного выполнения.
- Использовать multiprocessing, если куча задач, требующих интенсивных вычислений, и нужно преодолеть ограничения GIL.
- Использовать async, если нужно эффективно управлять большим количеством I/O-bound задач и минимизировать задержки.