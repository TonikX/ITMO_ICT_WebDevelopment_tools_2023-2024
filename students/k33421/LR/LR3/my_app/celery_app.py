import httpx
from bs4 import BeautifulSoup
from celery import Celery


app = Celery('tasks',
             result_backend=f"redis://redis:6379/0",
             broker='redis://redis:6379')


@app.task
def parse_url(url):
    with httpx.Client() as client:
        response = client.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text.strip()

    return {"data": title}
