import requests
from bs4 import BeautifulSoup
from connection import DBConn
from celery_app import celery_app


@celery_app.task
def parse(url):
    con = DBConn.connect_to_database()
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        articles = soup.find_all('article', class_='tm-articles-list__item')
        for article in articles:
            author = article.find('a', class_='tm-user-info__username').text
            datetime = article.find('a', class_='tm-article-datetime-published tm-article-datetime-published_link').text
            title = article.find('a', class_='tm-title__link').text
            with con.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, author, datetime))
        con.commit()
    except Exception as e:
        print("Ошибка:", e)
        con.rollback()
    con.close()
