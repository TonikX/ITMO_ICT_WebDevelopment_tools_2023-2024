from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select
import requests

import sys
sys.path.append("../..")

from connection import get_session
from models import *


router = APIRouter()

@router.post('/parser')
def parse(usernames: List[str]) -> TypedDict('Response', {"status": int, "msg": str}):
    try:
        response = requests.post('http://parser:80/parse', json=usernames)

        return {"status": 200, "msg": response.text}
    except:
        raise HTTPException(status_code=404, detail="Parsing failed")
        