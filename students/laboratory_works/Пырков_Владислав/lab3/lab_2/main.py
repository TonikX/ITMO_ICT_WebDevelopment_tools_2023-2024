from fastapi import FastAPI, BackgroundTasks
from parse import parse_and_save
app = FastAPI()


@app.post("/parse/")
async def parse(url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(parse_and_save, url)
    return {"message": "Parse started."}