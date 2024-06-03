from pydantic import BaseModel


class Healthcheck(BaseModel):
    ok: str
