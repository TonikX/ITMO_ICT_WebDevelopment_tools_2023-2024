from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from celery_worker import app as celery_app
from tasks import predict


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/api/predict')
async def create_prediction(ingredients_joined: str = '', url_to_send_results_to: str = ''):
    task = predict.delay(ingredients_joined, url_to_send_results_to=url_to_send_results_to)
    return JSONResponse(status_code=202, content={'task_id': task.id, 'status': task.status})


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
