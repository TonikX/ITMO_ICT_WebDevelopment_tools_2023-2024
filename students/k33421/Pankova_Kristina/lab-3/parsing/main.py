from fastapi import FastAPI, HTTPException
import requests
import multiprocessing
import psycopg2
from bs4 import BeautifulSoup
import re
import time
import os

app = FastAPI()

@app.post("/parse")
def parse(data: dict):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        response = requests.get(url)
        parse_and_save(url)
        return {"message": "Parsing completed"}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

urls = [
    'https://career.habr.com/vacancies?s%5B%5D=2&s%5B%5D=3&s%5B%5D=82&s%5B%5D=4&s%5B%5D=5&s%5B%5D=72&s%5B%5D=1&s%5B%5D=75&s%5B%5D=6&s%5B%5D=77&s%5B%5D=7&s%5B%5D=83&s%5B%5D=84&s%5B%5D=8&s%5B%5D=85&s%5B%5D=73&s%5B%5D=9&s%5B%5D=86&s%5B%5D=106&type=all',
    'https://career.habr.com/vacancies?s[]=2&s[]=3&s[]=82&s[]=4&s[]=5&s[]=72&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=84&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&s[]=106&sort=salary_desc&type=all',
    'https://career.habr.com/vacancies?s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true',
    'https://career.habr.com/vacancies?locations[]=c_699&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true'
]

#db_host = os.getenv("DB_HOST", "host.docker.internal") если хотим достучаться до локальной бд вне докера
db_host = os.getenv("DB_HOST", "0.0.0.0")
db_name = os.getenv("DB_NAME", "finance_db")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "1234")

conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)
c = conn.cursor()

def parse_and_save(url):
    # Реализация парсера из предыдущего кода
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
    conn.commit()
    print(f"Сохранен")

def main():
    start_time = time.time()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    conn.close()
    end_time = time.time()
    print(f"Время парсинга: {end_time - start_time:.2f} секунд")

if __name__ == '__main__':
    main()
