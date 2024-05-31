from book_parser import *
import time


def parse_and_save(url):
    book_details = get_book_details(url)
    if book_details:
        save_to_db([book_details])
        print(f"Saved book: {book_details['title']}")


start_time = time.time()
urls = fetch_random_book_ids(20)

for url in urls:
    parse_and_save(url)

print(f"Naive time: {time.time() - start_time}")
