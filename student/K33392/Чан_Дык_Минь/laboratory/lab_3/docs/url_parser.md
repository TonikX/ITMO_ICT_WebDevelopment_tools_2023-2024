### `url_parser/main.py`

Этот файл настраивает Celery worker и определяет задачу для парсинга URL.

- **Настройка Celery**: Инициализирует приложение Celery с Redis в качестве брокера сообщений и хранилища результатов.
- **Класс TripDTO**: TypedDict для определения ожидаемой структуры данных разобранной поездки.
- **Задача parse_url**: Определяет задачу Celery, которая принимает URL, делает HTTP GET запрос к URL, парсит HTML контент для извлечения заголовка страницы и возвращает его в качестве пункта назначения в словаре TripDTO.


```python
from celery import Celery # type: ignore
from typing import Optional, TypedDict # type: ignore
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore

# Demo url: https://www.tsarvisit.com/en/visits/the-hermitage-408

celery_app = Celery(
    'url_parser',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

class TripDTO(TypedDict):
    departure: Optional[str] = "Home"
    destination: str

@celery_app.task
def parse_url(url: str) -> Optional[TripDTO]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    destination = soup.title.string
    if not destination:
        return
    return {
        "destination": destination
    }
```

### `web_api/trips/routes.py`
Этот файл определяет API маршруты для приложения FastAPI, включая маршрут для вызова задачи парсинга URL.

- **Класс URLRequest**: Класс SQLModel для приема URL ввода.
- **Эндпоинт parse_trip_from_url**: 
  - Принимает URL, вызывает задачу Celery parse_url,
  - задача отправляется в очередь Redis, и Celery worker принимает и выполняет её, 
  - результат анализа сохраняется в backend Redis и отмечается как выполненный,
  - FastAPI проверяет состояние задачи через AsyncResult.

```python
class URLRequest(SQLModel):
    url: str

@router.post('/trip/parse', tags=["parse"])
async def parse_trip_from_url(url: URLRequest):
    task = parse_url.delay(url.url)
    result = AsyncResult(task.id)
    res = result.get()

    if not res:
        raise HTTPException(status_code=404, detail="No trips parsed")

    return {"result": res}
```