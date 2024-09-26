# Вызов парсера из FastAPI

**Эндпоинт в FastAPI для вызова парсера**:

Необходимо добавить в FastAPI приложение ендпоинт, который будет принимать запросы с URL для парсинга от клиента, отправлять запрос парсеру (запущенному в отдельном контейнере) и возвращать ответ с результатом клиенту.

```python
@app.post("/parse")
def parse(url: str, background_tasks: BackgroundTasks, session=Depends(get_session)):
    try:
        background_tasks.add_task(parse_and_save, url, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Parsing started"}

```
