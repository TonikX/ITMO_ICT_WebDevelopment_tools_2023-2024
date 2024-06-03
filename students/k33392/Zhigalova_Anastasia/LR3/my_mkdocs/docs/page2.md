# parser/main.py

### Реализуем два основных эндпоинта для работы с задачами Celery и один маршрут для синхронного парсинга URL

1. Когда клиент отправляет POST-запрос на /celery-task с URL, создается асинхронная задача Celery для парсинга этого URL.
2. Клиент получает идентификатор задачи и может использовать его для проверки статуса задачи через GET-запрос на /celery-task-status/{task_id}.
3. Для синхронного парсинга URL клиент может отправить POST-запрос на /parse с URL

```
app = FastAPI()

class URLRequest(BaseModel):
    url: HttpUrl

@app.post("/celery-task")
async def celery_task_endpoint(request: URLRequest):
    try:
        print (request.url)
        task = celery_app.send_task('celery_app.parse_url_task', args=[str(request.url)])
        return {"task_id": task.id, "status": "Task has been submitted"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/celery-task-status/{task_id}")
async def get_celery_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == 'FAILURE':
        return {"task_id": task_id, "status": task_result.state, "error": str(task_result.result)}
    return {"task_id": task_id, "status": task_result.state, "result": task_result.result}


@app.post("/parse")
def parse(url: str, db: Session = Depends(get_session)):
    return parse_and_save(db=db, url=url)

```