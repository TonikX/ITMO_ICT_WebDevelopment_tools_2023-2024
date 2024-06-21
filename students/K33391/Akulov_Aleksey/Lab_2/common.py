import requests
from bs4 import BeautifulSoup
import psycopg2

URLS = ['https://www.ebay.com/sch/i.html?_nkw=phone&_pgn=',
        'https://www.ebay.com/sch/i.html?_nkw=shoes+men&_sop=12&_pgn=',
        'https://www.ebay.com/sch/i.html?_nkw=lego&_pgn=']

PAGES = [2, 3, 4, 5, 6, 7, 8]

BD_CON = "dbname=money_db user=postgres password=sobaka12345 host=localhost"

def pars_item(item):
    title_tag = item.find('div', class_='s-item__title')
    if title_tag:
        title_span = title_tag.find('span', {'role': 'heading'})
        if title_span:
            title_text = title_span.get_text()
        else:
            title_text = "Название не найдено"
    else:
        title_text = "Название не найдено"

    price = item.find('span', class_='s-item__price')
    if price:
        price_text = price.get_text()
    else:
        price_text = "Цена не найдена"

    return {"name": title_text,
            "price": price_text}


def insert_into_db(parsed_items):
    conn = psycopg2.connect(BD_CON)
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO items (name, price) VALUES (%s, %s)''',
                       [(item['name'], item['price']) for item in parsed_items])
    conn.commit()
    cursor.close()
    conn.close()

def parse_and_save(url):
    for page in PAGES:
        complete_url = f'{url}{page}'
        try:
            response = requests.get(complete_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error req: {complete_url}\n{e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('li', class_='s-item')

        parsed_items = []
        for item in items:
            item_res = pars_item(item)
            parsed_items.append(item_res)

        insert_into_db(parsed_items)


def create_db():
    conn = psycopg2.connect(BD_CON)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT,
        price TEXT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

create_db()