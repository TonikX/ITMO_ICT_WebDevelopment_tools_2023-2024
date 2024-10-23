from celery import Celery
from pydantic import RedisDsn
from dotenv import dotenv_values
import os
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime, timedelta
import random

redis_dsn = str(
    RedisDsn.build(
        scheme='redis',
        host=os.getenv('BK_HOST', 'localhost'),
        port=int(os.getenv('BK_PORT', 6379)),
        path='0',
    )
)

app = Celery(
    'queue',
    broker=redis_dsn,
    backend=redis_dsn,
)


@app.task
def parse(season_start: int, season_end: int, year: int) -> None:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 5432),
        dbname=os.getenv('DB_DATABASE', 'postgres'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
    )
    cur = conn.cursor()

    for season in range(season_start, season_end):
        month = 10
        while month != 8:
            url = f'https://www.mariinsky.ru/playbill/archive/?season={season}&month={month}&year={year}'

            page = requests.get(url, headers={'User-Agent': UserAgent().chrome})
            soup = BeautifulSoup(page.text, 'lxml')
            elems = soup.find_all('div', class_='row light day_row') + soup.find_all('div', class_='row dark day_row')
            for elem in elems:
                title = elem.find('div', class_='spec_name').text
                description = elem.find('div', class_='descr').text.replace('\n', ' ')

                time_div = str(elem.find('div', class_='time'))
                data = time_div[time_div.index('datetime="') + 10:time_div.index('" itemprop="')]
                time_start = datetime.strptime(data[:data.index('+')], '%Y-%m-%dT%H:%M:%S')
                planned_time_end = time_start + timedelta(hours=random.randint(1, 5))
                priority = 1
                creator_id = 'admin'

                cur.execute(f'SELECT id FROM timetableday WHERE date = \'{data[:data.index('T')]}\'')
                day_id = cur.fetchone()[0]
                cur.execute(
                    f'INSERT INTO public.task(title, description, day_id, time_start, planned_time_end, priority, creator_id) '
                    f'VALUES (\'{title}\', \'{description}\', {day_id}, \'{time_start}\', \'{planned_time_end}\', {priority}, \'{creator_id}\')')

            month += 1
            if month == 13:
                month = 1
                year += 1

    conn.commit()
    conn.close()