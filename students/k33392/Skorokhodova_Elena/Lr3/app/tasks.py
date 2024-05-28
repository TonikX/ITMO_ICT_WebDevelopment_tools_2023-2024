from celery import Celery
import requests
from bs4 import BeautifulSoup

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def parse_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return {"url": url, "title": title}
    except requests.RequestException as e:
        return {"error": str(e)}
