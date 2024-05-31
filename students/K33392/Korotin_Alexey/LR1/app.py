from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from pydantic import BaseModel

from datetime import time, date
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginData(BaseModel):
    login: str
    password: str


@app.post('/upload', status_code=status.HTTP_200_OK)
def upload_file(file: UploadFile):
    print(file.file.read())
    return file.filename


@app.post('/login', status_code=status.HTTP_200_OK)
def login(data: LoginData) -> LoginData:
    print(data.login, data.password)
    return data

