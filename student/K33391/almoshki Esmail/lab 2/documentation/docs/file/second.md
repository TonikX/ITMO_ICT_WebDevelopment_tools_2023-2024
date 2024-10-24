# Python Web Scraping and Database Insertion: Async, Multiprocessing, and Multithreading

This document provides examples of how to scrape URLs and save the results in a MySQL database using three different approaches:
- Asynchronous programming (`asyncio`)
- Multiprocessing
- Multithreading

---

## async_parser.py

This script demonstrates how to use `asyncio` and `aiohttp` to asynchronously scrape multiple URLs and save the data into a MySQL database.

### Code:

```python
from bs4 import BeautifulSoup
import requests
from time import time
from connection import get_engine 
import aiohttp
import mysql.connector
from urls import urls
import asyncio

async def parse_and_save(url: str):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as resp:
            try:
                cnx = get_engine()
                cursor = cnx.cursor()
                
                r = requests.get(url, timeout=10)
                html = BeautifulSoup(r.text, features="html.parser")
                title = html.title.string if html.title else "No title"
                
                query = """INSERT INTO urls (title, url) VALUES (%s, %s)"""
                cursor.execute(query, (title, url))
                cnx.commit()
                
                print(f"Saved: {title} from {url}")

            except requests.RequestException as e:
                print(f"Request failed for {url}: {e}")
            except mysql.connector.Error as db_err:
                print(f"Database error for {url}: {db_err}")
            finally:
                cursor.close()
                cnx.close()

async def main():
    start_time = time()
    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Total time taken: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
-

```

## multiprocessing.py

This script demonstrates how to use `multiprocessing` to concurrently scrape URLs and save the data into the MySQL database.

### Code:

```python
from bs4 import BeautifulSoup
import requests
from time import time
from connection import get_engine 
import multiprocessing
import mysql.connector
from urls import urls

def parse_and_save(url: str):
    try:
        cnx = get_engine()
        cursor = cnx.cursor()
        
        r = requests.get(url, timeout=10)
        html = BeautifulSoup(r.text, features="html.parser")
        title = html.title.string if html.title else "No title"
        
        query = """INSERT INTO urls (title, url) VALUES (%s, %s)"""
        cursor.execute(query, (title, url))
        cnx.commit()
        
        print(f"Saved: {title} from {url}")

    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
    except mysql.connector.Error as db_err:
        print(f"Database error for {url}: {db_err}")
    finally:
        cursor.close()
        cnx.close()

def main():
    start_time = time()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Total time taken: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
```

---

## multithreading.py

This script demonstrates how to use threading to concurrently scrape URLs and save the data into a MySQL database.

### Code:

```python
from bs4 import BeautifulSoup
import requests
from time import time
from connection import get_engine 
import threading
import mysql.connector
from urls import urls

def parse_and_save(url: str):
    try:
        cnx = get_engine()
        cursor = cnx.cursor()
        
        r = requests.get(url, timeout=10)
        html = BeautifulSoup(r.text, features="html.parser")
        title = html.title.string if html.title else "No title"
        
        query = """INSERT INTO urls (title, url) VALUES (%s, %s)"""
        cursor.execute(query, (title, url))
        cnx.commit()
        
        print(f"Saved: {title} from {url}")

    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
    except mysql.connector.Error as db_err:
        print(f"Database error for {url}: {db_err}")
    finally:
        cursor.close()
        cnx.close()

def main():
    start_time = time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Total time taken: {time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
```
