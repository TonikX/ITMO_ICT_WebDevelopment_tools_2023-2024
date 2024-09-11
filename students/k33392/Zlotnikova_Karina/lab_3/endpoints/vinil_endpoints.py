from fastapi import APIRouter
from worker import parse

vinil_router = APIRouter()

@vinil_router.get("/parse/{page_num}")
async def parse_vinil(page_num: int):
    url = None
    if page_num == 1:
        url = 'https://vinyl.ru/catalog/'
    if page_num <=5 and page_num > 1:
        url = f'https://vinyl.ru/catalog/?PAGEN_1={page_num}'
    if url:
        parse.delay(url)
        return {"ok": True}
