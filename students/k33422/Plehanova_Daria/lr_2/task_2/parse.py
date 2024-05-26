import random
import uuid
from datetime import date

from bs4 import BeautifulSoup


def extract_user_data(page):
    soup = BeautifulSoup(page, 'html.parser')

    results = []

    for i, card in enumerate(soup.select('div.card-n__body')):
        name, age = (
            card
            .select_one('p.card-n__title.card-n__title--find.companion')
            .get_text(strip=True)
            .split(', ')
        )
        city = (
            card
            .select_one('li.card-n__info-item.city')
            .get_text(strip=True)
            .replace('Откуда:', '').strip())

        results.append(
            {
                'email': f'{str(uuid.uuid4())[:8]}@mail.ru',
                'first_name': name,
                'birth_date': date(date.today().year - int(age), 1, 1).strftime('%Y-%m-%d'),
                'description': city
            }
        )

    return results
