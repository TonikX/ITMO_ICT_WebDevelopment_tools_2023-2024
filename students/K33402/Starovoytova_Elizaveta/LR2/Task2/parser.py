import requests
from bs4 import BeautifulSoup
import json


def parse_author_info(url):
    # Отправляем GET-запрос к веб-странице
    response = requests.get(url)

    # Создаем объект BeautifulSoup для парсинга содержимого страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем имя автора
    author_name = soup.find('h1', class_='Author_authorName__i4Wxb').text.strip()

    # Извлекаем список книг
    books_elements = soup.find_all('p', class_='ArtInfoTile_title__TCqN1')
    books = [book.text.strip() for book in books_elements]

    # Формируем словарь с данными об авторе и его книгах
    author_data = {
        'author_name': author_name,
        'books': books
    }

    # Преобразуем словарь в JSON
    json_data = json.dumps(author_data, ensure_ascii=False)

    return json_data
