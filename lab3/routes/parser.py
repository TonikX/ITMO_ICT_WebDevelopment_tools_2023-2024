from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
import asyncio
from models import Site
import aiohttp
from bs4 import BeautifulSoup

router = APIRouter()

async def parse_and_save_async(url: str, session) -> str:
    async with aiohttp.ClientSession() as aio_session:
        response = await fetch_page(aio_session, url)
        soup = BeautifulSoup(response, 'html.parser')
        title_tag = soup.title
        if title_tag:
            title = title_tag.string
        else:
            title = ""  # or some default value
        site = Site(url=url, title=title, method='async')
        session.add(site)
        session.commit()
        session.refresh(site)
        return title  # Return the title value
async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, ssl=False) as response:
        return await response.text()

@router.get("/parse")
async def parse_current_site(session=Depends(get_session)) -> str:
    url = "http://127.0.0.1:8000/docs"  # current site URL
    title = await parse_and_save_async(url, session)
    return f"Successfully parsed and saved {url} with title {title}"
