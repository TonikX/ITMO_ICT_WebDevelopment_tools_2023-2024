import requests
from bs4 import BeautifulSoup
import time
import secrets
import string
import random
from multiprocessing import Process

from db_insert import insert_data

def get_condition():
    conditions = ['excellent', 'good', 'used']
    return random.choice(conditions)

def gen_password(n):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(n))
    return password

def parse_and_save(urls):
    for url in urls:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        new_username = soup.find('div', class_='info').find('h2').text
        new_email = f'{gen_password(5)}@example.com'
        new_password = gen_password(10)
        new_library_name = soup.find('span', class_='current book-rating-title').text
        new_book_name = soup.find('a', class_='title-link d-inline-block').text
        new_book_author = soup.find('a', class_='text-dark link').text
        new_book_condition = get_condition()

        data = []   # data = [('user7', 'user7@example.com', 'password7', 'library7', 'book1', 'author1', 'excellent')]
        entry = new_username, new_email, new_password, new_library_name, new_book_name, new_book_author, new_book_condition
        data.append(entry)
        insert_data(data)

def main(num):
    urls = [
        'https://readrate.com/rus/ratings/chto-chitaet-pink',
        'https://readrate.com/rus/ratings/lili-kollinz-knigi-na-polke-aktrisy',
        'https://readrate.com/rus/ratings/kakie-knigi-chitaet-emi-shumer',
        'https://readrate.com/rus/ratings/silvestr-stallone-lyubimye-knigi-zvezdy-boevikov',
        'https://readrate.com/rus/ratings/kventin-tarantino-lyubimye-knigi-metra-kino',
        'https://readrate.com/rus/ratings/tom-kruz-filmy-po-knigam-s-ego-uchastiem'
        ]
    beg = 0
    step = int(len(urls) / num)
    processes = []
    for _ in range(num):
        end = beg + step
        processes.append(Process(target=parse_and_save, args=(urls[beg:end], )))
        beg = end
    start = time.time()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    finish = time.time() - start
    print(f'Time: {round(finish, 4)}; number of processes: {num}')


if __name__ == '__main__':
    main(3)