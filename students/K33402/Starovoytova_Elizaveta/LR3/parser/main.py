from fastapi import FastAPI
import uvicorn
from database.conn import init_db
from endpoints.parser_api import parser_router


app = FastAPI()

app.include_router(parser_router, prefix="/api/parser", tags=["parser"])


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8002, reload=True)
