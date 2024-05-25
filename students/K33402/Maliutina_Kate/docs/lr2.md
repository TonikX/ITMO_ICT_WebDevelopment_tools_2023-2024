# Лабораторная часть

Ниже представлен код с подробными комментариями и скрины рабочие.
## task1/async1.py
```python
```

## task1/multiprocessing1.py
```python
```

## task1/threading1.py
```python
```

## task2/async2.py
```python
```

## task2/multiprocessing2.py
```python
```

## task2/threading2.py
```python
```

## task2/data.py
```python
# Список всех ссылок, по которым мы будем собирать данные
URLs = [
    'https://www.bookvoed.ru/catalog/knigi-s-avtografom-4435',
    'https://www.bookvoed.ru/catalog/detskie-knigi-1159',
    'https://www.bookvoed.ru/catalog/samoobrazovanie-i-razvitie-4560',
    'https://www.bookvoed.ru/catalog/khobbi-i-dosug-4056',
    'https://www.bookvoed.ru/catalog/estestvennye-nauki-1347',
    'https://www.bookvoed.ru/catalog/religiya-1437',
]

# Количество потоков/единиц выполнения
number_of_threads = 3
```

## task2/connection.py
```python
import psycopg2

# Класс базы данных
class DBConn:
    # SQL команда для вставки книг, %s будут заменять на переданные параметры
    # public - схема в бд, books - таблица внутри схемы
    INSERT_SQL = """INSERT INTO public.books(title, price) VALUES (%s, %s)"""

    # Аннотация/декоратор статического метода - метод, который не привязан к состоянию экземпляра или класса
    # (не нужна ссылка на сам класс 'self')
    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="web_books_db",  # название бд
            user="ekaterinamalyutina",  # имя пользователя
            password="postgres",  # пароль пользователя
            host="localhost",  # хост
            port="5432"  # дефолтный порт
        )  # подключаемся к этой бд и возвращаем эту связь
        return conn
```

# Screenshots
