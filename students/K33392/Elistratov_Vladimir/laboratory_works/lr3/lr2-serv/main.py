from fastapi import FastAPI, BackgroundTasks
from Models.Url import Link
from scripts.main import parse_urls_task
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

#region City
@app.post("/Cities/parse-url")
def getTravels(link: Link, background_tasks: BackgroundTasks):
    background_tasks.add_task()
    return "Success!"
#endregion
