import os
from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from db import insert_data
from dotenv import load_dotenv

load_dotenv()

# функция для парсинга и сохранения данных
def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    insert_data(url, title)

# главная функция для запуска парсинга в нескольких потоках
def main(urls):
    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()  # запускаем поток

    # ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    urls = [
        'https://career.habr.com/vacancies?s%5B%5D=2&s%5B%5D=3&s%5B%5D=82&s%5B%5D=4&s%5B%5D=5&s%5B%5D=72&s%5B%5D=1&s%5B%5D=75&s%5B%5D=6&s%5B%5D=77&s%5B%5D=7&s%5B%5D=83&s%5B%5D=84&s%5B%5D=8&s%5B%5D=85&s%5B%5D=73&s%5B%5D=9&s%5B%5D=86&s%5B%5D=106&type=all',
        'https://career.habr.com/vacancies?s[]=2&s[]=3&s[]=82&s[]=4&s[]=5&s[]=72&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=84&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&s[]=106&sort=salary_desc&type=all',
        'https://career.habr.com/vacancies?s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true',
        'https://career.habr.com/vacancies?locations[]=c_699&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true'
    ]

    start_time = time.time()
    main(urls)  # запускаем главную функцию
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tread: {execution_time}")
