from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from parsers import BtcComParser, BlockchainComParser
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


class ParserType(Enum):
    BTC_COM = "btccom"
    BLOCKHAIN_COM = "blockchaincom"

    def get_parser(self) -> BtcComParser | BlockchainComParser | None:
        if self.value == "btccom":
            return BtcComParser()
        if self.value == "blockchaincom":
            return BlockchainComParser()
        return None
        

class ParseRequest(BaseModel):
    parser: ParserType


@app.post("/parse")
async def parse(data: ParseRequest):
    if (parser := data.parser.get_parser()) is None:
        raise HTTPException(500, "invalid parser specified")
    return [i.model_dump() for i in await parser.aio_parse()]
