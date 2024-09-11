from fastapi import FastAPI, BackgroundTasks
from parse import parse_and_save
from db import get_session, Parce
from fastapi import Depends, status

app = FastAPI()

@app.post("/parse-url/")
async def parse(url: str, background_tasks: BackgroundTasks, session=Depends(get_session)):
    background_tasks.add_task(parse_and_save, url, session)
    return {"message": "Parse started."}


@app.get("/check/")
def cases_list(session=Depends(get_session)) -> list[Parce]:
    return session.query(Parce).all()