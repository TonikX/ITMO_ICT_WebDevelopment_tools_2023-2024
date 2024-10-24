from celery import Celery
from typing import Literal
from parsers import BtcComParser, BlockchainComParser

app = Celery("parser")

@app.task
def parse(parser_type: Literal["btccom", "blockchaincom"]):
    parser = None
    if parser_type == "btccom":
        parser = BtcComParser()
    elif parser_type == "blockchaincom":
        parser = BlockchainComParser()

    return [i.model_dump() for i in parser.parse()]

