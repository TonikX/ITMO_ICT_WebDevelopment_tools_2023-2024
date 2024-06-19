from fastapi import APIRouter

from parser.parser import parse_author_info
from database.save_data import save_author_and_books_from_json

parser_router = APIRouter()


@parser_router.post("/parse")
def parse(url: str):
    author_info = parse_author_info(url)
    save_author_and_books_from_json(author_info)
    return {"message": "Parsing completed"}