from pydantic import BaseModel

class UrlRequest(BaseModel):
    url: str

class ArticleResponse(BaseModel):
    id: int
    url: str
    title: str