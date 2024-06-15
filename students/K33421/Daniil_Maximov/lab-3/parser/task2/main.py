import time

import httpx
from bs4 import BeautifulSoup

from task2.db import recreate_database
from task2.async_worker import AsyncWorker
from task2.multiprocess_worker import MultiprocessWorker
from task2.threading_worker import ThreadingWorker


def get_article_urls_from_page(page: int) -> list[str]:
    feed = httpx.get(f"https://habr.com/ru/feed/page{page}/")

    soup = BeautifulSoup(feed.text, 'html.parser')

    a_tags = soup.find_all('a', attrs={'data-article-link': 'true'}, href=True)

    urls = []

    for a_tag in a_tags:
        if a_tag['href'].startswith('/ru/articles/'):
            urls.append(a_tag['href'])

    return list(map(lambda href: f"https://habr.com{href}", urls))


def get_random_article_urls(count: int) -> list[str]:
    urls = []

    i = 1

    while len(urls) < count:
        urls.extend(get_article_urls_from_page(i))
        i += 1

    return urls


def main():
    n_tasks = 2

    number_of_articles = 10

    urls = get_random_article_urls(number_of_articles)

    workers = [
        AsyncWorker(n_tasks, urls),
        MultiprocessWorker(n_tasks, urls),
        ThreadingWorker(n_tasks, urls),
    ]

    for worker in workers:
        recreate_database()

        print(f"Running {worker.__class__.__name__}")
        start_time = time.time()
        worker.run()
        end_time = time.time()
        print(worker.__class__.__name__, end_time - start_time, "\n")


if __name__ == '__main__':
    main()
