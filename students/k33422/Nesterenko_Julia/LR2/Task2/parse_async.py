import asyncio
import aiohttp
import random
from time import time
import pandas as pd

from parse_basic import *
from db_conn import save_stays_async, save_transitions_async


async def parse_and_save_async(key, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            if key == "planes":
                data = parse_planes(soup)
                await save_transitions_async(data)
            if key == "cruises": 
                data = parse_cruises(soup)
                await save_transitions_async(data)
            if key == "trains": 
                data = parse_trains(soup)
                await save_transitions_async(data)
            if key == "airbnb":
                data = parse_airbnb(soup)
                await save_stays_async(data)
            if key == "hotels": 
                data = parse_hotels(soup)
                await save_stays_async(data)
            if key == "hostels": 
                data = parse_hostels(soup)
                await save_stays_async(data) 


async def parse_chunk(chunk):
    for key, url in chunk:
        await parse_and_save_async(key, url)


async def check_n_splits(n):
    print(n, "SPLITS")
    start = time()
    keys = list(URLS.keys())
    random.shuffle(keys)
    chunks = [keys[i:i + len(URLS) // n] for i in range(0, len(URLS), len(URLS) // n)]
    chunks = [[(k, URLS[k]) for k in c] for c in chunks]
    await asyncio.gather(*(parse_chunk(chunk) for chunk in chunks))
    return n, time() - start


if __name__ == "__main__": 
    results = {}
    for n in [2, 3, 6]:
        loop = asyncio.get_event_loop()
        splits, extime = loop.run_until_complete(check_n_splits(n))
        results[splits] = extime
    print(pd.DataFrame({"Splits": results.keys(), "Execution Time": results.values()}))
    print()