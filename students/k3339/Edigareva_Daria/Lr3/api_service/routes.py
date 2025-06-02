from __future__ import annotations

from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from repository import ParseRepository as Repo
from requests import ParseAsyncCreate, ParseSyncQuery
from responses import (
    ParseAsyncResponse,
    StatusResponse,
    ResultResponse,
    SyncResult,
)
from tasks import parse_url_task

PARSER_HTTP = "http://parser:8001/fetch"

router = APIRouter()


@router.post("/parse_async")
async def parse_async(
        payload: ParseAsyncCreate,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> ParseAsyncResponse:
    req = await Repo.create(session, str(payload.url))
    parse_url_task.delay(req.id, str(payload.url))
    return ParseAsyncResponse(request_id=req.id, status=req.status)


@router.get("/status/{request_id}")
async def status(
        request_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> StatusResponse:
    obj = await Repo.by_id(session, request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return StatusResponse(request_id=obj.id, status=obj.status)


@router.get("/result/{request_id}")
async def result(
        request_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> ResultResponse:
    obj = await Repo.by_id(session, request_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")

    return ResultResponse(
        request_id=obj.id,
        status=obj.status,
        title=obj.title,
        html=obj.html_content,
    )


@router.get("/parse_sync")
async def parse_sync(
        query: Annotated[ParseSyncQuery, Query()],
) -> SyncResult:
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        try:
            resp = await client.get(PARSER_HTTP, params={"url": query.url})
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    data = resp.json()
    return SyncResult(url=query.url, title=data["title"], html=data["html"])
