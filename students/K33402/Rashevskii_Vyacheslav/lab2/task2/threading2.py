import threading
import time
from connection import DB
import requests
from bs4 import BeautifulSoup
from urls import URLs


def parse_and_save_threading(url, con):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(soup.find('title').text)  # сохранять заголовок страницы в базу данных по мне бесполезно
        # т.к. нагрузки 0 полезной, поэтому вывожу в консоль
        prs = soup.find_all('div', class_='Box-row Box-row--focus-gray p-0 mt-0 js-navigation-item js-issue-row')
        for pr in prs:
            title = (pr.find('a',
                             class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title').
                     text)
            span_text = pr.find('span', class_='opened-by').text.split()
            date = span_text[2] + ' ' + span_text[3][:-1] + ' ' + span_text[4]
            author = span_text[6]
            with con.cursor() as cursor:
                cursor.execute(DB.INSERT_SQL, (title, date, author))

        con.commit()
    except Exception as e:
        print("Exception caught: ", e)


def process_url_list_threading(url_list, con):
    for url in url_list:
        parse_and_save_threading(url, con)


def main_threading():
    count_for_1_thread = 2
    urls_for_1_thread = [URLs[i:i + count_for_1_thread] for i in range(0, len(URLs), count_for_1_thread)]

    con = DB.connect()

    threads = []
    for urls in urls_for_1_thread:
        thread = threading.Thread(target=process_url_list_threading, args=(urls, con))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    con.close()


if __name__ == '__main__':
    start_time = time.time()
    main_threading()
    end_time = time.time()
    print(f"Time of execution 'threading': {end_time - start_time} seconds")
