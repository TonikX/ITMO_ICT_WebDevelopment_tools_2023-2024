import time

import httpx

from task2.async_solution import AsyncSolution
from task2.database_connection import drop_create_tables
from task2.multiprocessing_solution import MultiprocessingSolution
from task2.threading_solution import ThreadingSolution


def get_random_article_url():
    return str(httpx.Client(follow_redirects=True).head("https://en.wikipedia.org/wiki/Special:Random").url)


def main():
    n_tasks = 2

    number_of_articles = 2

    urls = [get_random_article_url() for _ in range(number_of_articles)]

    print(urls)

    solutions = [
        AsyncSolution(n_tasks, urls),
        MultiprocessingSolution(n_tasks, urls),
        ThreadingSolution(n_tasks, urls),
    ]

    for solution in solutions:
        drop_create_tables()

        print(f"Running {solution.__class__.__name__}")
        start_time = time.time()
        solution.run()
        end_time = time.time()
        print(solution.__class__.__name__, end_time - start_time, "\n")


if __name__ == '__main__':
    main()
