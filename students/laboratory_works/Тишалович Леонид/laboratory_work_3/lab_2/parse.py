import requests
from bs4 import BeautifulSoup
from celery_main import celery_app
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='Bakugan102!',
        host='db',
        port='5432'
    )

def insert_data(url, title):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''INSERT INTO "site" (url, title) VALUES (%s, %s)
    ''', (url, title))
    conn.commit()
    cur.close()
    conn.close()

@celery_app.task
def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    insert_data(url, title)




