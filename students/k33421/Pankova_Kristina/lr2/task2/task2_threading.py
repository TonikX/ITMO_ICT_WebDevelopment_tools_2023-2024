import threading
import requests
from bs4 import BeautifulSoup
import psycopg2
import re
import time

urls = [
    'https://career.habr.com/vacancies?s%5B%5D=2&s%5B%5D=3&s%5B%5D=82&s%5B%5D=4&s%5B%5D=5&s%5B%5D=72&s%5B%5D=1&s%5B%5D=75&s%5B%5D=6&s%5B%5D=77&s%5B%5D=7&s%5B%5D=83&s%5B%5D=84&s%5B%5D=8&s%5B%5D=85&s%5B%5D=73&s%5B%5D=9&s%5B%5D=86&s%5B%5D=106&type=all',
    'https://career.habr.com/vacancies?s[]=2&s[]=3&s[]=82&s[]=4&s[]=5&s[]=72&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=84&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&s[]=106&sort=salary_desc&type=all',
    'https://career.habr.com/vacancies?s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true',
    'https://career.habr.com/vacancies?locations[]=c_699&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true'
]

conn = psycopg2.connect(
    host="localhost",
    database="finance_db",
    user="postgres",
    password="1234"
)
c = conn.cursor()

def parse_and_save(url):
    start_time = time.time()
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    vacancies = soup.find_all('a', {'class': 'vacancy-card__title-link'})
    salaries = soup.find_all('div', {'class': 'basic-salary'})
    for idx, vac in enumerate(vacancies):
        if salaries[idx].text:
            s = salaries[idx].text
        else:
            s = 100000
        print(vac.text, s)
        c.execute("INSERT INTO financialtransaction (description, amount, user_id) VALUES (%s, %s, %s)", (str(vac.text), re.findall(r'\d+', str(s))[0], 2))
    title = soup.title.string
    conn.commit()
    print(f"Сохранен титул '{title}' из {url}")
    end_time = time.time()
    print(f"Время парсинга: {end_time - start_time:.2f} секунд")

def main():
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    conn.close()

if __name__ == '__main__':
    main()
