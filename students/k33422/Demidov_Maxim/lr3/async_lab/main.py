from fastapi import FastAPI, HTTPException
import requests

from async_handlers import data_handlers
from task2_asyncio import parse_all_urls

app = FastAPI()


@app.get("/")
def greeting():
    return '''Hello, you can parse data from /parse/{category} endpoint, 
                    where category can be 'users','teams', 'projects', 'tasks', 'userprofiles'.'''


@app.post("/parse/{category}")
async def parse(category: str):
    try:
        handler_func = data_handlers.get(category)
        if not handler_func:
            raise HTTPException(status_code=404, detail="Category not found")
        url_to_parse = f"https://async-lab.tiiny.site/{category}"
        added = await parse_all_urls(handler_func, url_to_parse, 5)
        return {"message": "Parsing completed", "added_count": added}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
