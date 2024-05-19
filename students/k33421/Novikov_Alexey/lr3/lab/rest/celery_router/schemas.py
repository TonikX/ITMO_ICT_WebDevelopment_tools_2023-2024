from pydantic import BaseModel


class TaskIdResponse(BaseModel):
    task_id: str


class TaskStatusResponse(BaseModel):
    status: str


class ParsedDataResponse(BaseModel):
    data: str
