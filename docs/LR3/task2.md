# Вызов парсера из FastAPI

**Эндпоинт в FastAPI для вызова парсера**:

Необходимо добавить в FastAPI приложение ендпоинт, который будет принимать запросы с URL для парсинга от клиента, отправлять запрос парсеру (запущенному в отдельном контейнере) и возвращать ответ с результатом клиенту.

```python
@app.post("/parse/")
async def parse(
    url: str, background_tasks: BackgroundTasks, session=Depends(get_session)
):
    background_tasks.add_task(parse_and_save, url, session)
    return {"message": "Parsing started."}
```
