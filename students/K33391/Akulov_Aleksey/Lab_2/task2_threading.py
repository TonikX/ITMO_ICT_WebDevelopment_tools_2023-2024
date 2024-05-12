import threading
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Определение моделей здесь
# Подключение к базе данных
engine = create_engine('sqlite:///your_database.db')
Session = sessionmaker(bind=engine)


def parse_and_save(url):
    session = Session()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text if soup.find('title') else 'No title found'

    # Сохранение заголовка в базу данных
    # Например, создание новой транзакции или пользователя
    new_user = User(username=title, password='dummy')
    session.add(new_user)
    session.commit()
    session.close()
    print(f'Processed {url}: {title}')


def main_threading(urls):
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


urls = ['https://example.com', 'https://example.org', 'https://example.net']
main_threading(urls)
