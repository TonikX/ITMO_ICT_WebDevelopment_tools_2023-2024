import requests
from bs4 import BeautifulSoup
from celery_app import celery_app
from connection import DataBaseConnection


def get_bio(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('div', class_='xZmPc')
    bio_container = text.find('div')
    if bio_container.em and bio_container.em.text:
        return bio_container.em.text
    if bio_container.text:
        return bio_container.text

@celery_app.task
def parse_url_task(url: str):
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    db_conn = DataBaseConnection.connect_to_database()

    tasks = soup.find_all('div', class_='CHPy6')
    for task in tasks:
        name = task.find('div', class_='dbENL').text + ' ' + task.find('div', class_='p1Gbz').text
        bio = get_bio('https://www.culture.ru' + task.a['href'])

        with db_conn.cursor() as cursor:
                cursor.execute(DataBaseConnection.INSERT_SQL, (name, bio))

    db_conn.commit()