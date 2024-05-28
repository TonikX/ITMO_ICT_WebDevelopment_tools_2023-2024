# Структура файла запуска
Довольно прозаично
```Python
import models
from connection import *
from routes import router
import uvicorn


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/") # для тестирования
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


```
