from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import *


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("title").text

    conn = psycopg2.connect("postgresql://postgres:1@localhost:5432/web_data")
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()


def main(urls):
    num_process = len(urls) if len(urls) < 4 else 4
    pool = Pool(processes=num_process)
    pool.map(parse_and_save, urls)


if __name__ == "__main__":
    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time
    file = open("times.txt", "a")

    file.write(f"Multiprocessing time: {execution_time}\n")
