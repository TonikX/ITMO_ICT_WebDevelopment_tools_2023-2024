from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel, HttpUrl
import aiohttp
import ssl
from auth import AuthHandler

parser_router = APIRouter()
auth_handler = AuthHandler()

class URLItem(BaseModel):
    url: HttpUrl

async def fetch_title_from_parser(url):
    parser_url = "http://parser:9000/get-title/"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.post(parser_url, json={"url": url}) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Error fetching the title from parser")
            data = await response.json()
            return data.get("task_id")

async def get_task_status(task_id):
    parser_url = f"http://parser:9000/status/{task_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(parser_url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Error fetching task status")
            data = await response.json()
            return data

@parser_router.get("/status/{task_id}", tags=['parser'])
async def get_status(task_id: str):
    status = await get_task_status(task_id)
    return status

@parser_router.post("/fetch-title/", tags=['parser'])
async def fetch_title(url_item: URLItem):
    task_id = await fetch_title_from_parser(str(url_item.url))
    return {"task_id": task_id}