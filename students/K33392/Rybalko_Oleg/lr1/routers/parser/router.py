from fastapi import APIRouter
from .models import ParseRequest
import aiohttp

router = APIRouter(prefix="/parse")

@router.post("")
async def parse(req: ParseRequest):
    async with aiohttp.ClientSession() as client:
        async with client.post("http://parser:8080", json=dict(req)) as resp:
            return await resp.json()

