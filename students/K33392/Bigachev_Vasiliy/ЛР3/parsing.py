import psycopg2
import requests
from bs4 import BeautifulSoup

from time import sleep

db_url = "dbname=lr1 user=postgres password=1 host=db"
#db_url = "dbname=lr1 user=postgres password=1"

# Avito
URLS = [ 
    "https://www.avito.ru/sankt-peterburg?q=%D0%A7%D0%B0%D0%B9",
    "https://www.avito.ru/sankt-peterburg?q=%D0%9A%D0%BE%D1%84%D0%B5",
    "https://www.avito.ru/sankt-peterburg?q=%D0%93%D0%B0%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8",
    "https://www.avito.ru/sankt-peterburg?q=%D0%A1%D0%BE%D0%BA",
    "https://www.avito.ru/sankt-peterburg?q=%D0%92%D0%BE%D0%B4%D0%B0"
]

# Ebay
URLS2 = [
    "https://www.ebay.com/sch/i.html?_from=R40&_nkw=%D0%A7%D0%B0%D0%B9&_sacat=0&_pgn=1",
    "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=%D0%9A%D0%BE%D1%84%D0%B5&_sacat=0&_odkw=%D0%A7%D0%B0%D0%B9&_osacat=0",
    "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=%D0%A1%D0%BE%D0%BA&_sacat=0&_odkw=%D0%93%D0%B0%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B0&_osacat=0",
    "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=%D0%9A%D0%BD%D0%B8%D0%B3%D0%B8&_sacat=0&_odkw=%D0%A1%D0%BE%D0%BA&_osacat=0",
    "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=%D0%9A%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B&_sacat=0&_odkw=%D0%9A%D0%BD%D0%B8%D0%B3%D0%B8&_osacat=0"
]

# Avito
def pars_item_avito(item):
    # Парсинг названия
    title_tag = item.find('div', class_='iva-item-title-CdRXl')
    if not title_tag:
        print("NOT FOUND")
    title_h3 = title_tag.find('h3')
    if not title_h3:
        print("NOT FOUND")
    title_text = title_h3.get_text()
    if not title_text:
        print("NOT FOUND")
    # Прасинг цены
    price_tag = item.find('div', class_='price-price-j2OjU')
    if not price_tag:
        print("NOT FOUND")
    price_meta = price_tag.find('meta', itemprop='price')
    if not price_meta:
        print("NOT FOUND")
    if price_meta["content"] == 0:
        return {"title": title_text, "price": 1}
    else:
        return {"title": title_text, "price": price_meta["content"]}

# Ebay
def pars_item_ebay(item):
    title_tag = item.find('div', class_="s-item__title")
    title_span = title_tag.find('span', role='heading')
    title_text = title_span.get_text()
    price_tag = item.find('span', class_='s-item__price')
    price_text = price_tag.get_text()
    
    return {'title': title_text, 'price': price_text}

def insert_into_db(parsed_items):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    for item in parsed_items:
        try:
            cursor.execute('''INSERT INTO items (name, price) VALUES (%s, %s)''', (item["title"], item["price"]))
        except:
            continue
    conn.commit()
    cursor.close()
    conn.close()

def parse_and_save(url):
    items = []
    while items == []:
        print("Отправляем запрос")
        try:
            response = requests.get(url)
            print("Status code: " + str(response.status_code))
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            print(f"Error req: {url}\n{e}")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Avito
        #items = soup.find_all('div', class_='iva-item-body-GQomw')
        
        # Ebay
        items = soup.find_all('li', class_='s-item')
        
        if items == []:
            print("Не нашлись items")
            f = open("test_results.txt", 'w', encoding="utf-8")
            f.write(str(soup))
            f.close()
            return 0
        
    
    parsed_items = []
    for item in items:
        
        # Avito
        #item_res = pars_item_avito(item)
        
        # Ebay
        item_res = pars_item_ebay(item)
        parsed_items.append(item_res)
    
    #print(parsed_items)
    insert_into_db(parsed_items)
    
# Вывод информации из базы данных
def select_items():
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM items
    ''')
    rows = cursor.fetchall()
    print("Items in dbss")
    for row in rows:
        print(row)
    conn.commit()
    cursor.close()
    conn.close()

# Создание базы данных
def create_db():
    conn = psycopg2.connect(db_url)
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