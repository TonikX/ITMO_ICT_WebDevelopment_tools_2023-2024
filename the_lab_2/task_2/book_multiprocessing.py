import multiprocessing
import time
from book_parser import *


import multiprocessing


def parse_and_save_multiprocessing(book_id):
    book_data = get_book_details(book_id)
    if book_data:
        save_to_db([book_data])
        print(f"Saved: {book_data['title']}")


def parse_and_save(book_ids):
    start_time = time.time()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(parse_and_save_multiprocessing, book_ids)
    pool.close()
    pool.join()

    print(f"Multiprocessing version took {time.time() - start_time}")


if __name__ == "__main__":
    urls = fetch_random_book_ids(20)
    parse_and_save(urls)
