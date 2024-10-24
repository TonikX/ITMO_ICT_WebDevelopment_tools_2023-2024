import asyncio as aio
from aio_conn import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from parsers import BlockchainComParser, BtcComParser, AbstractParser

async def parse_and_save(parser: AbstractParser, session: AsyncSession):
    parsed_data = await parser.aio_parse()
    for d in parsed_data:
        session.add(d)
    # await session.commit()

async def main():
    blockchain_parser = BlockchainComParser()
    btc_parser = BtcComParser()
    session = await anext(get_session())
    task1 = aio.create_task(parse_and_save(blockchain_parser, session))
    task2 = aio.create_task(parse_and_save(btc_parser, session))
    await aio.gather(task1, task2)

if __name__ == "__main__":
    aio.run(main())
