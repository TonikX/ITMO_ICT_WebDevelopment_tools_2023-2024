from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    url: HttpUrl