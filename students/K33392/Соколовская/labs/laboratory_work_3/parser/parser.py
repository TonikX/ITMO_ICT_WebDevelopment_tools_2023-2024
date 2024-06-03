import requests
from bs4 import BeautifulSoup
import json


def parse_data(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    author_name = soup.find('h1', class_='Author_authorName__i4Wxb').text.strip()

    books_elements = soup.find_all('p', class_='ArtInfoTile_title__fVt0C')
    books = [book.text.strip() for book in books_elements]

    author_data = {
        'author_name': author_name,
        'books': books
    }

    json_data = json.dumps(author_data, ensure_ascii=False)

    return json_data
