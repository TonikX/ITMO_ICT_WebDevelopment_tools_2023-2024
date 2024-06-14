import requests
from bs4 import BeautifulSoup
from db import DB
from celery_app import celery_app


@celery_app.task
def parse_and_save_threading(url):
    con = DB.connect()
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'html.parser')
    prs = soup.find_all('div', class_='Box-row Box-row--focus-gray p-0 mt-0 js-navigation-item js-issue-row')
    for pr in prs:
        title = (pr.find('a',
                         class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title').
                 text)
        span_text = pr.find('span', class_='opened-by').text.split()
        date = span_text[2] + ' ' + span_text[3][:-1] + ' ' + span_text[4]
        author = span_text[6]
        with con.cursor() as cursor:
            cursor.execute(DB.INSERT_SQL, (title, date, author))
    con.commit()
    con.close()
