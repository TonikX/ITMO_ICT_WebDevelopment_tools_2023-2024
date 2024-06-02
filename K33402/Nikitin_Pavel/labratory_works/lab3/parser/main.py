from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from tasks import fetch_and_store_title

app = FastAPI()

class URLItem(BaseModel):
    url: HttpUrl

@app.post("/get-title/")
async def get_title(url_item: URLItem):
    result = fetch_and_store_title.delay(str(url_item.url))
    print(result, "RESULT")
    return {"task_id": str(result)}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task_result = fetch_and_store_title.AsyncResult(task_id)
    if task_result.state == 'PENDING':
        return {"status": "PENDING"}
    elif task_result.state == 'SUCCESS':
        return {"status": "SUCCESS", "result": task_result.result}
    else:
        return {"status": "FAILURE"}
