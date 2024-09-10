import requests
from bs4 import BeautifulSoup
from db import DBConn
from celery_app import celery_app


@celery_app.task
def parse_and_save_threading(url):
    db_conn = DBConn.connect_to_database()
    try:  # пробуем, поскольку может упасть исключение
        page = requests.get(url)  # получаем страницу
        soup = BeautifulSoup(page.text, 'html.parser')  # создаем парсер
        books = soup.find_all('div', class_='product-card')  # находим все блоки книг по классу
        for book in books:  # проходимся в цикле по всем книгам
            title = book.attrs['data-product-name']  # получаем название книги
            price = book.attrs['data-product-price-discounted']  # получаем цену книги

            with db_conn.cursor() as cursor:  # через специальный класс cursor получаем доступ к базе данных
                cursor.execute(DBConn.INSERT_SQL, (title, price))  # выполняем ранее написанную команду и передаем в нее аргументы

        db_conn.commit()  # подтверждаем изменения
    except Exception as e:  # при получении исключения
        print("Ошибка:", e)  # выводим ошибку
        db_conn.rollback()  # откатываем изменения
    finally:
        db_conn.commit()
        db_conn.close()
