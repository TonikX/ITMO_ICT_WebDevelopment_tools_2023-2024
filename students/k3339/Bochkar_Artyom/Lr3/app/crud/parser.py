import httpx
from fastapi import APIRouter

from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter()


class RequestURL(BaseModel):
    url: str


@router.post("/parse")
async def parse_url(request: RequestURL):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://parser:8001/parse",
                json={"url": request.url},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Parser service error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/parse-async")
async def parse_url_async(request: RequestURL):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://parser:8001/parse-async",
                json={"url": request.url},
                timeout=30.0
            )
            response.raise_for_status()
            return {"message": "Parse request sent", "response": response.json()}

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Parser service error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/task/{task_id}")
async def proxy_task_status(task_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://parser:8001/task/{task_id}")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ошибка при обращении к парсеру: {e}")