from pydantic import BaseModel
from typing import Literal

class ParseRequest(BaseModel):
    parser: Literal["btccom", "blockchaincom"]

