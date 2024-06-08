**Подзадача 3: Вызов парсера из FastAPI через очередь**

Как это работает
Celery и Redis:

Celery — это асинхронная очередь задач, которая позволяет легко распределять и выполнять задачи в фоне. Redis используется как брокер сообщений, хранящий задачи, которые должны быть выполнены.
При получении HTTP-запроса, задача ставится в очередь Redis, и Celery-воркер обрабатывает её в фоне.
Docker Compose:

Docker Compose позволяет легко настроить и запустить Celery, Redis и ваше FastAPI приложение как отдельные контейнеры, работающие в одной сети. Это упрощает управление зависимостями и конфигурацией всех компонентов системы.
Почему это важно для студентов
Практические навыки настройки и использования асинхронной очереди задач в реальном приложении - первый шаг для MLops для 45 направления. Студенты научатся разделять ответственность между различными сервисами и компоновать их для достижения общей цели. В реальных проектах часто требуется выполнение сложных и длительных операций. Опыт работы с Celery и Redis подготовит к решению таких задач и даст уверенность в использовании современных технологий.

**Задание**

- Установить Celery и Redis:

Необходимо добавить зависимости для Celery и Redis в проект. Celery будет использоваться для обработки задач в фоне, а Redis будет выступать в роли брокера задач и хранилища результатов.

**Зачем:** Celery и Redis позволяют организовать фоновую обработку задач, что полезно для выполнения длительных или ресурсоемких операций без блокировки основного потока выполнения.

- Настроить Celery:

необходимо создать файл конфигурации для Celery. Определть задачу для парсинга URL, которая будет выполняться в фоновом режиме.
**Зачем:** Настройка Celery позволит асинхронно обрабатывать задачи, что улучшит производительность и отзывчивость вашего приложения.

- Обновить Docker Compose файл:

Необходимо добавить сервисы для Redis и Celery worker в docker-compose.yml. Определите зависимости между сервисами, чтобы обеспечить корректную работу оркестра.

**Зачем:** Это позволит вам легко управлять всеми сервисами вашего приложения, включая асинхронную обработку задач, с помощью одного файла конфигурации.

- Эндпоинт для асинхронного вызова парсера:

Необходимо добавить в FastAPI приложение маршрут для асинхронного вызова парсера. Маршрут должен принимать запросы с URL для парсинга, ставить задачу в очередь с помощью Celery и возвращать ответ о начале выполнения задачи.
**Зачем:** Это позволит запускать парсинг веб-страниц в фоне, что улучшит производительность и пользовательский опыт вашего приложения.

<hr>
<hr>

**celery_config.py**
```
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "tasks.parse_url": {"queue": "parser_queue"},
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
```

**tasks.py**
```
from celery_config import celery_app
from sqlalchemy.orm import Session
from connection import SessionLocal
from parser import parse_and_save

@celery_app.task
def parse_url_task(url: str):
    db: Session = SessionLocal()
    try:
        parse_and_save(url, db)
    finally:
        db.close()
```

В main.py появился путь:
```
@app.post("/parse/async/")
def parse_urls_async(urls: List[str]):
    task_ids = []
    for url in urls:
        task = parse_url_task.delay(url)
        task_ids.append(task.id)
    return {"message": "Parsing tasks started", "task_ids": task_ids}
```

В docker_compose.py
```
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"

  worker:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:12345678@db:5432/recipes
    command: ["celery", "-A", "tasks.celery_app", "worker", "--loglevel=info"]
```

Где-то тут -- традиционно уже -- у меня включилось любопытство. Поэтому я стала замерять время выполнения парсинга, и появился дополнительный путь, чтобы сравнить разницу между наивным и асинхронным выполнением.

```
@app.post("/parse/async/")
def parse_urls_async(urls: List[str]):
    start_time = time.time()

    task_ids = []
    for url in urls:
        task = parse_url_task.delay(url)
        task_ids.append(task.id)

    end_time = time.time()
    timer = end_time - start_time
    return {"message": "Parsing tasks started", "task_ids": task_ids, "Execution time": f"{timer:.2f}"}


@app.post("/parse/naive/")
def parse_urls_async(urls: List[str], db: Session = Depends(get_db)):
    start_time = time.time()

    for url in urls:
        parse_and_save(url, db)

    end_time = time.time()
    timer = end_time - start_time
    return {"message": "Parsing tasks started", "Execution time": f"{timer:.2f}"}
```