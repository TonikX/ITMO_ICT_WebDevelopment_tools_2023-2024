import asyncio
from time import time
from db import get_connnection, close_connection, create_trip, insert_trip_async
from parser import parse_trips_async
import aiosqlite


RUNS_NUMBER = 3
CHUNKS_NUMBER = 4
PAGES_NUMBER = 16


async def parse_and_save(urls):
    parsed_trips = []
    for url in urls:
        next_parsed_trips = await parse_trips_async(url)
        parsed_trips = [*parsed_trips, *next_parsed_trips]

    # conn = get_connnection()
    async with aiosqlite.connect('db.sqlite') as conn:
        for trip in parsed_trips:
            trip_to_insert = create_trip(trip)
            await insert_trip_async(conn, trip_to_insert)
    # close_connection(conn)
    return 'success'


async def main():
    tasks = []
    base_url = 'https://bolshayastrana.com/tury?plainSearch=1&page='
    urls = [base_url + str(i + 1) for i in range(PAGES_NUMBER)]

    for i in range(CHUNKS_NUMBER):
        chunk_len = len(urls) / CHUNKS_NUMBER
        task = asyncio.create_task(parse_and_save(urls[int(i*chunk_len):int((i+1)*chunk_len)]))
        tasks.append(task)

    start = time()
    res = await asyncio.gather(*tasks)
    exec_time = time() - start

    return exec_time, res


if __name__ == "__main__":
    times = []
    for i in range(RUNS_NUMBER):
        next_time, res = asyncio.run(main())
        times.append(next_time)
        print(i + 1, ' run: ', next_time, 's. RESULT: ', res)
    print('Average time: ', sum(times) / len(times), 's')


