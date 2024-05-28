from pydantic import BaseModel
from enum import Enum

class ParserType(Enum):
    BTC_COM = "btccom"
    BLOCKHAIN_COM = "blockchaincom"


class ParseRequest(BaseModel):
    parser: ParserType

