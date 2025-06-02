from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from parser import fetch_html_and_title
from requests import FetchQuery
from responses import FetchResponse

router = APIRouter()


@router.get("/fetch", summary="Скачать страницу и вернуть HTML")
async def fetch(query: Annotated[FetchQuery, Query(...)]) -> FetchResponse:
    try:
        title, html = await fetch_html_and_title(str(query.url))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return FetchResponse(url=query.url, title=title, html=html)
