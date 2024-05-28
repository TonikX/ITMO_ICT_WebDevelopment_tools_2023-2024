from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from celery_worker import app as celery_app
from tasks import predict


app = FastAPI()


@app.post('/api/predict')
async def create_prediction(ingredients_joined: str = ''):
    task = predict.delay(ingredients_joined)
    return JSONResponse(status_code=202, content={'task_id': task.id, 'status': task.status,})


@app.get('/api/result/{task_id}')
async def get_result(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': task_id, 'status': task.status, 'result': None})
    result = task.get()
    return JSONResponse(status_code=200, content={'task_id': task_id, 'status': task.status, 'result': result['result']})


@app.get('/api/status/{task_id}')
async def get_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)
    return JSONResponse(status_code=200, content={'task_id': task_id, 'status': task.status})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
