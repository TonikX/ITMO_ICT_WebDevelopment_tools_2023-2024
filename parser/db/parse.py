from pydantic import BaseModel


class ParseRequest(BaseModel):
    url: str