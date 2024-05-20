from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_entries = soup.find_all("article", class_="product_pod")

    for entry in book_entries:

        title_tag = entry.find("h3")
        book_title = title_tag.find("a")["title"]

        price_tag = entry.find("p", class_="price_color")
        book_price = price_tag.text.strip("Â£")

        conn = psycopg2.connect("dbname=books_info user=postgres password=qwerty12345 host=localhost")
        curs = conn.cursor()

        curs.execute("INSERT INTO books (title, price) VALUES (%s, %s)", (book_title, book_price))
        conn.commit()

        curs.close()
        conn.close()

        if entry == book_entries[0]:
            print(f"Book Title: {book_title}")
            print(f"Book Price: {book_price}")
            print()


def main(pages):

    threads = []
    for page in pages:
        thread = Thread(target=parse_and_save, args=(f'https://books.toscrape.com/catalogue/category/books_1/page-{page}.html',))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":

    pages = [1, 2, 3, 4]

    start_time = time.time()
    main(pages)
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Threading time: {execution_time}")
