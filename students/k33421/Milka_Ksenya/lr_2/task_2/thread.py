import threading
import time

from . import parse, database


def iteration(page: int):
    content = parse.get_content(page)

    data_list = parse.parse_data(content)

    for data in data_list:
        database.insert_data_to_project(data)


def main():
    tasks = [threading.Thread(target=iteration, args=(page,)) for page in range(1, 6)]

    start = time.perf_counter()
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    end = time.perf_counter()

    print(f"Время: {end - start}")


main()
