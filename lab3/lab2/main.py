from fastapi import FastAPI, BackgroundTasks
from parse import parse_and_save

app = FastAPI()

@app.post("/parse/")
async def parse(url: str, background_tasks: BackgroundTasks, session=None):
    background_tasks.add_task(parse_and_save, url, session)
    return {"message": "Parse started."}
