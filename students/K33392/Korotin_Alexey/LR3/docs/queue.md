# Очередь
Для парсинга была реализована Celery-задача.
Содержимое файла `celery_backend.tasks.py`
```python
def parse_page(url: str) -> WebPage:
    logger = logging.getLogger()
    logger.info('Requesting url %s', url)
    soup = BeautifulSoup(urlopen(url), features="html.parser")
    title = soup.title.get_text()
    logger.info('Got response with title \'%s\'', title)
    page = WebPage(title=title)
    return page


@app.task
def parse_task(url):
    return parse_page(url)
```

## Интерфейс очереди
Для работы с очередью был предоставлен публичный HTTP-API на базе FastApi.
Он содержит в себе следующие эндпоинты:
- `POST /tasks` - поместить задачу на парсинг в очередь. В результате выполнения будет возвращен уникальный идентификатор операции
- `GET /tasks/{task_id}` - получить результат выполнения задачи по её уникальному идентификатору

## Пример работы
В качестве демонстрации получим информацию о Государственном бюджете Казахстана.
URL `https://openbudget.kz/data/`

### Шаг 1 - поместим задачу в очередь
Для этого отправим HTTP-запрос на эндпоинт /tasks
![img.png](img.png)
В ответ получим уникальный идентификатор созданной задачи в формате UUID (`5f0c7599-7533-4b9d-b0c3-0cd20cbb05e8`)
![img_1.png](img_1.png)
## Шаг 2 - получим результат выполнения задачи
Для этого обратимся ко второму эндпоинту /tasks/{task_id} с полученным нами ранее уникальным идентификатором задачи
![img_2.png](img_2.png)
В качестве ответа получаем заголовок запрашиваемой нами HTML-страницы.
![img_3.png](img_3.png)