# Вызов парсера из FastAPI через очередь

## Celery в FastAPI

```python
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_routes={
        "parse.parse_and_save": "main-queue",
    },
)

```

### Инициализация парсера с Celery

```python
@celery_app.task
def parse_and_save(url, session):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title"

    new_article = Parse(url=url, article_title=title)

    session.add(new_article)
    session.commit()

```
