# app/celery_client.py и app/Dockerfile

### Настраиваем маршрутизацию для API - два маршрута: один для отправки URL на парсинг, а другой для проверки статуса задачи.

```
PARSER_SERVICE_URL = "http://parser:8000/celery-task"

router = APIRouter()

@router.post("/parse-url")
def parse_url(url: str):
    try:
        response = requests.post(PARSER_SERVICE_URL, json={"url": url})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=505, detail=str(e))

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    response = requests.get(f"http://parser:8000/celery-task-status/{task_id}")
    return response.json()
```


#### Dockerfile для app
```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN mount=type=cache,target=/root/.cache pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```